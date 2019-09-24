from src.stream.Stream import *
import sys
import datetime
from scipy.stats import norm


#TODO: Reconsider step size, collection size, more fine grained than per-second input time_window.
# Represents a peripheral, plugged in some uPnP device.
# Keeps track of received packets from that peripheral in self.collection.
# self.collection : [ [ (1, timestamp),... ] , [ (1, timestamp), ... ], ... ]
# At the position of the reference index (~ 1/3 of len(self.collection), the time corresponds to the peripheral sampling period.
# Indexes before that represent previous moments in time: every index to the left is self.step time units away from the next.
# Indexes after that represent next moments in time: every index to the left is self.step time units away from the next.
# The time represented by these indexes is not absolute time, but time_difference between consecutive packets.
class StreamFixedK(Stream):


    def __init__(self, peripheral_id, device_id, sampling_rate, alpha, beta, lats, state, constraintsToK):
        self.peripheral_id = peripheral_id
        self.device_id = device_id
        self.sampling_rate = sampling_rate #i.e. 60s
        self.latencies = lats
        # used to specify when packets are received (by taking the difference with current time)
        # instantiate at system time when created, but re-instantiated upon first packet received
        self.timer = datetime.datetime.now()
        # used to bootstrap parameters for window computation
        self.initiated = False
        self.empty = True
        self.constraintsToK = {}
        for constraint in constraintsToK:
            self.constraintsToK[float(constraint)] = constraintsToK[constraint]



        #self.constraintToK = {"0.1":, "0.2":, "0.3:", "0.4:", "0.5":, "0.6":, "0.7":, "0.8":, "0.9":, "1.0":}
        # self.adapt_state = False
        # TODO: configurable
        # nb of std's above or below the estimated mean to count for triggering adaptation
        #self.adapt_factor = 3
        # nb of times the threshold was violated
        #self.nb_violations = 0
        #self.K = 140

        #self.moving_accuracy = {"1.0": None, "0.75": None, "0.5": None, "0.25": None}
        self.window_size = 100
        #self.accuracies = {"1.0": [], "0.75": [], "0.5": [], "0.25": []}

        self.packet_received = False

        # dictionary that maps completeness levels (keys) to TimeWindows (values)
        # by default, keeps track of "1.0"
       # self.completenessToTimeWindow = {"1.0": None, "0.75": None, "0.5": None, "0.25": None }
        self.completenessToTimeWindow = dict()
        for constraint in constraintsToK.keys():
            self.completenessToTimeWindow[constraint] = None
        # reverse of above, key is TimeWindow and value is completeness.
        # by default, track sr + 2, sr, sr -2, sr - 4, sr - 6
        self.timeWindowToCompleteness = {str(sampling_rate + 2): None, str(sampling_rate): None, str(sampling_rate - 2): None, str(sampling_rate - 4): None, str(sampling_rate - 6): None}

        # parameters for past window computation (according to TCP EWMA approach)
        self.R = None
        # SRTT, mean
        self.smoothedArrivalTime = sampling_rate
        # to be tweaked from looking at historic data
        self.alpha = alpha
       # self.alpha_original = alpha
        # to be tweaked from looking at historic data
        self.beta = beta
        #self.beta_original = beta
        # to be tweaked to specify past window size (dependence on variance).
        # self.K = K
        # RTTVAR
        self.arrivalTimeVariance = 0

        # in case no packets are received in the past window

        self.lastUpdatePeriod = sys.maxsize
        self.lastRelativeTime = 0

        self.state = state
        self.state.addAlpha(self.peripheral_id + '|' + self.device_id, self.alpha)
        self.state.addBeta(self.peripheral_id + '|' + self.device_id, self.beta)
        #self.state.addK(self.peripheral_id + '|' + self.device_id, self.K)
       # self.state.addSamplingRate(self.peripheral_id + '|' + self.device_id, self.sampling_rate)

    def updateMovingAverage(self, completeness):
        values = []
        timestamps = []
        # print('len(accuracies[1.0]):', len(self.accuracies['1.0']))
        # print('len(accuracies[0.75]):', len(self.accuracies['0.75']))
        # print('len(accuracies[0.5]):', len(self.accuracies['0.5']))
        # print('len(accuracies[0.25]):', len(self.accuracies['0.25']))
        for ac in self.accuracies[completeness]:
            values.append(ac[0])
            timestamps.append(ac[1])
        cumsum, moving_aves = [0], []

        for i, x in enumerate(values, 1):
            cumsum.append(cumsum[i - 1] + x)
            if i >= self.window_size:
                moving_ave = (cumsum[i] - cumsum[i - self.window_size]) / self.window_size
                # can do stuff with moving_ave here
                moving_aves.append((moving_ave, timestamps[i - 1]))
        #print('Moving Accuracy[', completeness, ']:', moving_aves)
        if len(moving_aves) > 0:
            self.moving_accuracy[completeness] = moving_aves[0][0]
            moving_accuracy = (moving_aves[0][0], moving_aves[0][1])
            self.state.addMovingAccuracy(self.peripheral_id + '|' + self.device_id, completeness, moving_accuracy)


    # to be called when first packet arrives
    # initializes parameters for TCP EWMA algorithm to compute pastWindow.
    def initialize(self, arrival_time):
        self.smoothedArrivalTime = arrival_time
        #TODO: replace with more sensible initial value, i.e. 1s
        #arrivalTimeVariance = round(abs(arrival_time - float(self.sampling_rate))/2,2)
        #arrivalTimeVariance = abs(arrival_time - self.sampling_rate)

        #arrivalTimeVariance = abs(arrival_time - self.lastRelativeTime) / 2
        # initialized as the latency of the first packet received divided by 2, following RTO RFC.
        arrivalTimeVariance = float(self.latencies[0][0]) / 2

        #print('init atvar:', arrivalTimeVariance)

        self.arrivalTimeVariance = arrivalTimeVariance


    # between 0 and 1.0
    def trackCompletenessPercentage(self, percentage):
        self.completenessToTimeWindow[percentage] = None

    def getCompletenessToTimeWindow(self):
        return self.completenessToTimeWindow

    def getTimeWindowtoCompleteness(self):
        return self.timeWindowToCompleteness

    #AIMD for alpha: divide by 2 (like TCP), increase by 0.1
    def increaseAlpha(self):
        #print('min(self.alpha_original, self.alpha * 2)', min(self.alpha_original, self.alpha * 2))
        self.alpha = min(self.alpha_original, self.alpha + 0.1)
        #print('self.alpha increase:', self.alpha)

    def decreaseAlpha(self):
        #print('max(self.alpha/2, 0.1)', max(self.alpha/2, 0.1) )
        self.alpha = max(self.alpha/2, 0.1)
        #print('self.alpha decrease:', self.alpha)

    #TODO: Add methods to remove tracked TimeWindows/Completeness

    # checks if given arrival_time is
    def is_outlier(self, arrival_time):
        #print('arrival_time:', arrival_time)
       # print('self.smoothedArrivalTime + self.adapt_factor*self.arrivalTimeVariance', self.smoothedArrivalTime + self.adapt_factor*self.arrivalTimeVariance)
        #TODO: Uncomment to enable outlier detection based on STD
        #if abs(arrival_time  - self.smoothedArrivalTime) > self.adapt_factor*self.arrivalTimeVariance:
        if float(abs(arrival_time - self.smoothedArrivalTime) / self.smoothedArrivalTime) > 0.5 :
           # print('=== is_outlier====')
            #print('sat:', self.smoothedArrivalTime)
            #print('outlier:', arrival_time)
            # print('arrival time:', arrival_time)
            # print('sat:', self.smoothedArrivalTime)
            # print('atvar:', self.arrivalTimeVariance)
            return True
        return False

    def addAccuracy(self, accuracy, timestamp, completeness):
        #print('addAccuracy:', accuracy)
        if len(self.accuracies[completeness]) < self.window_size:
            self.accuracies[completeness].append((accuracy, timestamp))
            #print('self.accuracies: <100', self.accuracies)
        else:
            self.accuracies[completeness] = self.accuracies[completeness][1:]
            self.accuracies[completeness].append((accuracy, timestamp))
            #print('self.accuracies >100:', self.accuracies)

    # called upon whenever a new packet from this peripheral arrives.
    # it then triggers the (re)computation of the pastWindow, and updates self.collection accordingly.
    # returns True when all has been initialized, False otherwise
    def incrementCollection(self, rat, currentTime, timeToWrite):
       # if first packet received, start the timer
            timeReceived = rat
            time_difference = timeReceived - self.sampling_rate
            ### past
            # if not self.packet_received:
            #     self.packet_received = True
            #     self.lastRelativeTime = timeReceived

            if not self.initiated:
                self.initialize(timeReceived)
                self.lastRelativeTime = timeReceived
                self.initiated = True
                for key in self.getCompletenessToTimeWindow().keys():
                    new_key = key
                    #if (key == '1.0'):
                    #    new_key = 0.9999
                    # self.state.addTimeWindow(self.peripheral_id + '|' + self.device_id, key,
                    #                          (None, timeToWrite))
                    (newTimeWindow, K) = self.computeTimeWindow(float(new_key), currentTime)
                    self.completenessToTimeWindow[key] = newTimeWindow
                for key in self.getTimeWindowtoCompleteness().keys():
                    # self.state.addCompleteness(self.peripheral_id + '|' + self.device_id, key,
                    #                            (None, timeToWrite))
                    newCompleteness = self.computeProbability(float(key), currentTime)
                    self.timeWindowToCompleteness[key] = newCompleteness
                return False
            else:
                self.lastRelativeTime = timeReceived
                self.state.addSAT(self.peripheral_id + '|' + self.device_id, (self.smoothedArrivalTime, timeToWrite))
                #print('adding SAT:')
                self.state.addATVAR(self.peripheral_id + '|' + self.device_id, (self.arrivalTimeVariance, timeToWrite))
                self.lastArrivalTime = timeReceived
                self.updateArrivalTimeVariance()
                self.updateSmoothedArrivalTime()
                #print('sat:', self.smoothedArrivalTime)
               # self.state.addSAT(self.peripheral_id + '|' + self.device_id, (self.smoothedArrivalTime, timeToWrite))
                #self.state.addATVAR(self.peripheral_id + '|' + self.device_id, (self.arrivalTimeVariance, timeToWrite))
                # compute TimeWindows for tracked completeness levels
                for key in self.getCompletenessToTimeWindow().keys():
                    new_key = key
                    #print('constraint:', new_key)
                    (newTimeWindow, K) = self.computeTimeWindow(float(new_key), currentTime)
                    #print('time_window: ', newTimeWindow)
                    # print('new prediction: ' + str(newTimeWindow))
                    accuracy = 0

                    prediction_error = abs(self.completenessToTimeWindow[key] - rat)
                    if self.completenessToTimeWindow[key] >= rat:
                        accuracy = 1
#                   self.addAccuracy(accuracy, timeToWrite, key)
                  #  self.updateMovingAverage(key)
                    # self.completenessToAccuracy[key] = self.completenessToAccuracy[key] + (accuracy -
                    #                                                                        self.completenessToAccuracy[
                    #                                                                            key]) / self.nb_observations
                    self.state.addTimeWindow(self.peripheral_id + '|' + self.device_id, key,
                                             (self.completenessToTimeWindow[key], timeToWrite))
                    self.state.addAccuracyForTimeWindow(self.peripheral_id + '|' + self.device_id, key,
                                                        (accuracy, timeToWrite))
                    self.state.addK(self.peripheral_id + '|' + self.device_id, key,
                                    (K, timeToWrite))
                   # self.completenessToTimeWindow[key] = newTimeWindow
                    #self.state.addTimeWindow(self.peripheral_id + '|' + self.device_id, key, (self.completenessToTimeWindow[key], timeToWrite))
                    self.completenessToTimeWindow[key] = newTimeWindow
                # for key in self.getTimeWindowtoCompleteness().keys():
                #     newCompleteness = self.computeProbability(float(key), currentTime)
                #     self.state.addCompleteness(self.peripheral_id + '|' + self.device_id, key, (round(self.timeWindowToCompleteness[key],2), timeToWrite))
                #     self.timeWindowToCompleteness[key] = newCompleteness


    def trackCompleteness(self, timeWindow):
        self.timeWindowToCompleteness[timeWindow] = None

    def trackTimeWindow(self, completeness):
        self.completenessToTimeWindow[completeness] = None



    # obtain probability of data being present for given time_window
    # time_window in seconds
    # only takes into account packets that have arrived in the past self.pastWindow seconds.
    def computeProbability(self, time_window, currentTime):
       newCompleteness = round(norm.cdf(round(time_window, 2), self.smoothedArrivalTime, self.arrivalTimeVariance))
       return newCompleteness

    def getCompleteness(self, timeWindow):
        return self.timeWindowToCompleteness[timeWindow]


    # percentage in %
    # computes the TimeWindow (UpdatePeriod) that satisfies the given correctness requirement.
    def computeTimeWindow(self, completeness, currentTime):
        #newUpdatePeriod = round(norm.ppf(completeness,loc= self.smoothedArrivalTime, scale=self.arrivalTimeVariance), 2)
        #print('completeness:', completeness)

        # if completeness == 1.0:
        #      K = 10
        #else:
         #    K = norm.ppf(completeness, 0, 1)
        # if completeness == 0.75:
        #     K = 0.867
        # if completeness == 0.5:
        #     K = -0.28
        # if completeness == 0.25:
        #     K = -0.715
        # if completeness == 0.75:
        #     K = 2
        # if completeness == 0.5:
        #     K = 1.2
        # if completeness == 0.25:
        #     K = 0.6

        newUpdatePeriod = self.smoothedArrivalTime + self.constraintsToK[completeness]* self.arrivalTimeVariance
        #print('newUpdatePeriod', newUpdatePeriod)
        #print('self.sat', self.smoothedArrivalTime)
        #print('K', K)
        #print('self.arrivalTimeVariance', self.arrivalTimeVariance)
        return (newUpdatePeriod,self.constraintsToK[completeness])

        # SAT = alpha * SAT + (1-alpha)*R

    def updateSmoothedArrivalTime(self):
       # print(self.device_id, self.peripheral_id, 'SmAT:', self.smoothedArrivalTime)
        #print('self.alpha:', self.alpha)

        smoothedArrivalTime = round(self.alpha * self.smoothedArrivalTime + (1 - self.alpha) * self.lastArrivalTime,2)

        #print('self.smootherArrivalTime:', self.smoothedArrivalTime)
        self.smoothedArrivalTime = smoothedArrivalTime


        # ATVAR = beta * ATVAR + (1 - beta) * |SAT - R|

    def updateArrivalTimeVariance(self):
       # print(self.device_id, self.peripheral_id, 'ArrTVar:', self.arrivalTimeVariance)
       #  arrivalTimeVariance = round(self.beta * self.arrivalTimeVariance + (1 - self.beta) * abs(
       #      self.smoothedArrivalTime - self.lastArrivalTime),2)

        arrivalTimeVariance = round(self.beta * self.arrivalTimeVariance + (1 - self.beta) * abs(
           self.smoothedArrivalTime - self.lastArrivalTime), 2)
        self.arrivalTimeVariance = arrivalTimeVariance

    def getTimeWindow(self, completeness):
        return self.completenessToTimeWindow[str(completeness)]

    def getCompleteness(self, timeWindow):
        return self.timeWindowToCompleteness[str(timeWindow)]
