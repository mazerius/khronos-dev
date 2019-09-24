import datetime
from dateutil.parser import parse
from tqdm import tqdm



from src.core.State import *
from src.stream.StreamManager import *
from src.utils.parse import *

#from storage.InfluxDBWriter import *


class Simulation:

    def __init__(self, filename, lats_filename,id, approach, constraintsToK = None,timeouts=None, name=None):
        self.filename = filename
        self.latencies = lats_filename
        self.device_to_lat = dict()
        self.id = id
        self.state = State(filename, id, name)
        self.approach = approach
        #self.influxdb_client = InfluxDBWriter()
        self.stream_manager = StreamManager()
        self.device_to_rat = dict()
        self.sampling_rates = dict()
        self.constraintsToK = constraintsToK
       # self.alphas = dict()
       # self.betas = dict()
       # self.alpha = -1
       # self.beta = -1
        self.parsed_data_set = False
        #self.parameters = parameters
      #  self.timeouts = timeouts


    def initializeSimulationForDevice(self, device, data_set, approach):
        print(datetime.datetime.now(), ": Simulation", self.id, "started...")
        if not self.parsed_data_set:
            self.device_to_rat = self.parseDataSet(data_set)
            self.sampling_rates = self.parseSamplingRates()
            self.device_to_lat = self.parse_latencies_per_device()



        print('Preparing simulation objects...')
        peripheral_id = device.split('|')[0]
        address = device.split('|')[1]

            #global peripheral_manager
        if approach == 'ND_fixedK':
            self.stream_manager.createStreamFixedK(peripheral_id, address, self.sampling_rates[device],
                                                   float(7 / 8),
                                                   float(3 / 4), self.device_to_lat[device],
                                                   self.state, self.constraintsToK)


    def initializeSimulation(self, rats_filename, lats_filename, approach):
        print('Approach:', approach)
        print(datetime.datetime.now(), ": Simulation", self.id, "started...")
        self.device_to_rat = parseDataSet(rats_filename, self.state)
        print('Parsing sampling rates...')
        self.sampling_rates = parseSamplingRates(rats_filename, self.state)
        print('Parsing latency ')
        parseLatencies(lats_filename, self.state)
        print('Preparing simulation objects...')
        self.approach = approach
        for i in tqdm(range(len(list(self.sampling_rates.keys())))):
            device = list(self.sampling_rates.keys())[i]
            peripheral_id = device.split('|')[0]
            address = device.split('|')[1]
            try:
                if approach == 'fixedK':
                    self.stream_manager.createStreamFixedK(peripheral_id, address, self.sampling_rates[device],
                                                           float(7/8),
                                                           float(3/4), self.state.state[device]['lats'],
                                                           self.state, self.constraintsToK)
            except KeyError as err:
                print('KeyError:', err)


    def runSimulationForDevice(self, device_key):
        print('Running simulation...')
        timestamps = []
        device = device_key
        peripheral_id = device.split('|')[0]
        device_id = device.split('|')[1]
        max_rat = -1
        average_rat = 0
        #         # for rat in state.getRelativeArrivalTimes(device):
        #         #     average_rat += rat[0]
        #         #     if rat[0] >= max_rat:
        #         #         max_rat = rat[0]
        #         # average_rat = average_rat / len(state.getRelativeArrivalTimes(device))
        for rat in self.device_to_rat[device]:
            average_rat += rat[0]
            if rat[0] >= max_rat:
                max_rat = rat[0]
            # rat[1] = rat[1][1:len(rat[1])]
            yyyymmdd = rat[1].split('T')[0]
            hhmmssSSS = rat[1].split('T')[1]
            timestamp = yyyymmdd + ' ' + hhmmssSSS
            timeToWrite = datetime.datetime.strptime(rat[1].split('+')[0], '%Y-%m-%dT%H:%M:%S.%f')
            # print('timetoWrite pre:', timeToWrite)
            timeToWrite = timeToWrite.strftime('%Y-%m-%dT%H:%M:%S.%f')
            # print('timeToWrite:', timeToWrite)
            # print('rat:', rat)
            timestamps.append((timeToWrite))
            self.state.state[device]['relative_arrival_times_to_show'].append((rat[0], timeToWrite))
            self.stream_manager.getStreamByDeviceID(peripheral_id, device_id).incrementCollection(rat[0], float(
                parse(timestamp).strftime("%s")), timeToWrite)
        max_rats = []
        avg_rats = []
        average_rat = average_rat / len(self.state.getRelativeArrivalTimes(device))
        for timestamp in timestamps:
            max_rats.append((max_rat, timestamp))
            avg_rats.append((average_rat, timestamp))
        self.state.addMaxRelativeArrivalTime(device, max_rats)
        self.state.addAvgRelativeArrivalTime(device, avg_rats)


    def runSimulation(self):
        print('Running simulation...')
        for i in tqdm(range(len(list(self.device_to_rat.keys())))):
            timestamps = []
            device = list(self.device_to_rat.keys())[i]
            peripheral_id = device.split('|')[0]
            device_id = device.split('|')[1]
            max_rat = -1
            average_rat = 0
            #         # for rat in state.getRelativeArrivalTimes(device):
            #         #     average_rat += rat[0]
            #         #     if rat[0] >= max_rat:
            #         #         max_rat = rat[0]
            #         # average_rat = average_rat / len(state.getRelativeArrivalTimes(device))
            for rat in self.device_to_rat[device]:
                stream = self.stream_manager.getStreamByDeviceID(peripheral_id, device_id)
                if stream == None:
                    pass
                else:
                    average_rat += rat[0]
                    if rat[0] >= max_rat:
                        max_rat = rat[0]
                    #rat[1] = rat[1][1:len(rat[1])]
                    yyyymmdd = rat[1].split('T')[0]
                    hhmmssSSS = rat[1].split('T')[1]
                    timestamp = yyyymmdd + ' ' + hhmmssSSS
                    timeToWrite = datetime.datetime.strptime(rat[1].split('+')[0], '%Y-%m-%dT%H:%M:%S.%f')
                    #print('timetoWrite pre:', timeToWrite)
                    timeToWrite = timeToWrite.strftime('%Y-%m-%dT%H:%M:%S.%f')
                    #print('timeToWrite:', timeToWrite)
                    #print('rat:', rat)
                    timestamps.append((timeToWrite))
                    self.state.state[device]['relative_arrival_times_to_show'].append((rat[0], timeToWrite))
                    self.stream_manager.getStreamByDeviceID(peripheral_id, device_id).incrementCollection(rat[0], float(
                        parse(timestamp).strftime("%s")), timeToWrite)
            max_rats = []
            avg_rats = []
            average_rat = average_rat / len(self.state.getRelativeArrivalTimes(device))
            for timestamp in timestamps:
                max_rats.append((max_rat, timestamp))
                avg_rats.append((average_rat, timestamp))
            self.state.addMaxRelativeArrivalTime(device, max_rats)
            self.state.addAvgRelativeArrivalTime(device, avg_rats)

    def computePercentageBelowConstraint(self, ma, constraint):
        result = 0
        for ac in ma:
            if ac[0] < constraint:
                result += 1
        return round((float(result) / len(ma)), 7)

    def computePredictionError(self, preds, rats):
        result = []
        if not self.approach == 'oracle':
            rats = rats[1:]
        for i in range(0, len(preds)):
            result.append(abs(rats[i][0] - preds[i][0]))
            #result.append(preds[i][0] - rats[i][0])
            return round(sum(result) / len(result), 2)

    def movingAverage(self, accuracies, window_size):
        values = []
        timestamps = []
        for ac in accuracies:
            values.append(ac[0])
            timestamps.append(ac[1])
        cumsum, moving_aves = [0], []

        for i, x in enumerate(values, 1):
            cumsum.append(cumsum[i - 1] + x)
            if i >= window_size:
                moving_ave = (cumsum[i] - cumsum[i - window_size]) / window_size
                # can do stuff with moving_ave here
                moving_aves.append((moving_ave, timestamps[i - 1]))
        return moving_aves

    # compute accuracy, precision, prediction error for computed time windows
    # compute accuracy, precision for computed completeness
    def analyzeSimulation(self):
        print('Evaluating Timeout predictions...')
        #sleep(0.5)
        for i in tqdm(range(len(list(self.state.getState().keys())))):
            device = list(self.state.getState().keys())[i]
            for cc in self.state.state[device]['time_windows'].keys():
                cc = float(cc)
                rats = self.state.state[device]['relative_arrival_times']
                #print(self.state.state[device]['time_windows'].keys())
                accuracy = self.state.state[device]['time_windows'][cc]['accuracy']
                timouts = self.state.state[device]['time_windows'][cc]['prediction']
                mer = 0
                for ac in accuracy:
                    mer += ac[0]
                mer = round(1 - (mer / len(accuracy)), 2)
                pe = self.computePredictionError(timouts, rats)
                # if len(rats) >= 100:
                #     bc = 100*round(self.computePercentageBelowConstraint(self.movingAverage(accuracy, 100), cc), 2)
                # else:
                #     bc = None
                # self.state.state[device]['time_windows'][cc]['bc'] = bc
                self.state.state[device]['time_windows'][cc]['mer'] = mer
                self.state.state[device]['time_windows'][cc]['pe'] = pe



# compute accuracy, precision, prediction error for computed time windows
# compute accuracy, precision for computed completeness
    def analyzeSimulationForDevice(self, device_key):
        print('Evaluating Timeout predictions for', device_key, '...')
        device = device_key
        rats = self.device_to_rat[device]
        for completeness in self.state.getTimeWindows(device).keys():
            sum_accuracy = 0
            try:
                # filter out total_accuracy, total_precision keys
                val = float(completeness)
                # predictions
                tws = self.state.getTimeWindows(device)[completeness]['prediction']
                j = 0
                while (j < len(tws) - 1) :
                    #print('tw[j]:',tws[j])
                    #print('rats[j+1]:', rats[j+1])
                    tw = tws[j][0]
                    absolute_precision_error = abs(rats[j+1][0] - tw)
                    accuracy = 0
                    precision = 0

                    # error from constraint
                    precision_error = 0
                    if rats[j+1][0] != 0 :
                        precision = round(((rats[j][0] - abs(rats[j+1][0] - tw)) / rats[j][0]), 2)
                        #print('tw:', tw)
                    #print('rat:', rats[j+1][0])
                    if tw >= rats[j+1][0]:
                        accuracy = 1
                        sum_accuracy += 1
                    achieved_completeness = round(sum_accuracy / (j + 1), 2)
                    # absolute error
                    # precision_error = (achieved_completeness - val)
                    self.state.addAccuracyForTimeWindow(device, str(val), (accuracy, tws[j][1]))
                    self.state.addPredictionErrorForTimewindow(device, str(val), (absolute_precision_error, tws[j][1]))
                    self.state.addPrecisionForTimeWindow(device, str(val), (precision, tws[j][1]))
                    self.state.addAchievedCompletenessForCompletenessConstraint(device, str(val), (achieved_completeness, tws[j][1]))
#                        self.state.addPrecisionErrorForCompletenessConstraint(device, str(val), (precision_error, tws[j][1]))
                    j+=1
                #total_accuracy = total_accuracy / j
                #total_precision = total_precision / j
                #self.state.addTotalAccuracyTimeWindows(device, completeness, total_accuracy)
                #state.addTotalPrecisionTimeWindows(device, completeness, total_precision)
            except ValueError:
                pass

