

# Instantiates a Peripheral object for every peripheral in the network.
class State:


    def __init__(self, filename, id, name):
        self.state = dict()
        self.filename = filename
        self.id = id
        self.name = name


    def registerDevice(self, device):
        self.state[device] = dict()
        self.state[device]['relative_arrival_times'] = None
        self.state[device]['relative_arrival_times_to_show'] = []
        #self.state[device]['past_windows'] = []
        # keys are completeness levels
        self.state[device]['time_windows'] = dict()
        # keys are fixed timewindows
        self.state[device]['completeness'] = dict()
        #self.state[device]['alpha'] = None
        #self.state[device]['beta'] = None
        self.state[device]['sampling_rate'] = None
        self.state[device]['max_relative_arrival_time'] = None
        self.state[device]['avg_relative_arrival_time'] = None
        #self.state[device]['rm'] = False
        #print('SimulationModel', str(self.state))



    def removeDevice(self, device):
        self.state[device]['rm'] = True


    def getIndexForRat(self, device_key, timestamp):
        for i in range(0, len(self.state[device_key]['relative_arrival_times'])):
            if self.state[device_key]['relative_arrival_times'][i][1] == timestamp:
                print('found rat for timestamp!')
                return i
        return -1

    def getState(self):
        return self.state

    def getRelativeArrivalTimes(self, device_key):
        return self.state[device_key]['relative_arrival_times']

    def getTimeWindows(self, device_key):
        return self.state[device_key]['time_windows']

    def getCompleteness(self, device_key):
        return self.state[device_key]['completeness']

    def getBeta(self, device_key):
        return self.state[device_key]['beta']

    def getAlpha(self, device_key):
        return self.state[device_key]['alpha']

    def getK(self, device_key, cc):
        return self.state[device_key]['time_windows'][cc]['K']

    def getSamplingRate(self, device_key):
        return self.state[device_key]['sampling_rate']

    def getActualCompleteness(self,device_key, time_window):
        return self.state[device_key]['completeness'][time_window]['actual_completeness']

    def addSAT(self, device_key, sat):
        if not 'sat' in self.state[device_key].keys():
            self.state[device_key]['sat']= [sat]
        else:
            self.state[device_key]['sat'].append(sat)

    def getSAT(self, device_key):
        return self.state[device_key]['sat']

    def addATVAR(self, device_key, atvar):
        if not 'atvar' in self.state[device_key].keys():
            self.state[device_key]['atvar']= [atvar]
        else:
            self.state[device_key]['atvar'].append(atvar)

    def getATVAR(self, device_key):
        return self.state[device_key]['atvar']

    def getMovingAccuracy(self, device_key):
        return self.state[device_key]['moving_accuracy']

    def addK(self, device_key, cc, K):
        #print('str(self.state[device_key]', str(self.state[device_key]))
        if not 'K' in self.state[device_key]['time_windows'][cc].keys():
            self.state[device_key]['time_windows'][cc]['K']= [K]
        else:
            self.state[device_key]['time_windows'][cc]['K'].append(K)

    # accuracy = (value, timeToWrite)
    def addActualCompleteness(self, device_key, time_window, actual_completeness):
        #print("AADDDDING ACTUAL COMPLETENESSS")
        if not 'actual_completeness' in self.state[device_key]['completeness'][time_window].keys():
          #  print("NOT IN")
            self.state[device_key]['completeness'][time_window]['actual_completeness'] = [actual_completeness]
        else:
          #  print("ININININ")
            self.state[device_key]['completeness'][time_window]['actual_completeness'].append(actual_completeness)
        # accuracy = (value, timeToWrite)

    def addMovingAccuracy(self, device_key, completeness, moving_accuracy):
        if not 'moving_accuracy' in self.state[device_key]['time_windows'][completeness].keys():
            self.state[device_key]['time_windows'][completeness]['moving_accuracy'] = [moving_accuracy]
        else:
            self.state[device_key]['time_windows'][completeness]['moving_accuracy'].append(moving_accuracy)

            # accuracy = (value, timeToWrite)

    def addPredictionErrorForCompleteness(self, device_key, time_window, prediction_error):
        if not 'prediction_error' in self.state[device_key]['completeness'][time_window].keys():
            self.state[device_key]['completeness'][time_window]['prediction_error'] = [prediction_error]
        else:
            self.state[device_key]['completeness'][time_window]['prediction_error'].append(prediction_error)
            # accuracy = (value, timeToWrite)

    # accuracy = (value, timeToWrite)
    def addAccuracyForTimeWindow(self, device_key, completeness, accuracy):
       # print(str(self.state[device_key]))
        if not 'accuracy' in self.state[device_key]['time_windows'][completeness].keys():
            self.state[device_key]['time_windows'][completeness]['accuracy'] = [accuracy]
        else:
            self.state[device_key]['time_windows'][completeness]['accuracy'].append(accuracy)

            # accuracy = (value, timeToWrite)

    def addPrecisionErrorForCompleteness(self, device_key, completeness, precision_error):
        if not 'precision_error_true' in self.state[device_key]['time_windows'][completeness].keys():
            self.state[device_key]['time_windows'][completeness]['precision_error_true'] = [precision_error]
        else:
            self.state[device_key]['time_windows'][completeness]['precision_error_true'].append(precision_error)

    def addAchievedCompletenessForCompletenessConstraint(self, device_key, completeness, achieved_completeness):
        if not 'achieved_completeness' in self.state[device_key]['time_windows'][completeness].keys():
            self.state[device_key]['time_windows'][completeness]['achieved_completeness'] = [achieved_completeness]
        else:
            self.state[device_key]['time_windows'][completeness]['achieved_completeness'].append(achieved_completeness)

    def addPredictionErrorForTimewindow(self, device_key, completeness, precision_error):
        if not 'precision' in self.state[device_key]['time_windows'][completeness].keys():
            self.state[device_key]['time_windows'][completeness]['precision_error'] = [precision_error]
        else:
            self.state[device_key]['time_windows'][completeness]['precision_error'].append(precision_error)

    def addPrecisionForTimeWindow(self, device_key, completeness, precision):
        if not 'precision' in self.state[device_key]['time_windows'][completeness].keys():
            self.state[device_key]['time_windows'][completeness]['precision'] = [precision]
        else:
            self.state[device_key]['time_windows'][completeness]['precision'].append(precision)

    def getAccuracyForTimeWindow(self, device_key, completeness):
        return self.state[device_key]['time_windows'][completeness]['accuracy']

    def getPrecisionForTimeWindow(self, device_key, completeness):
        return self.state[device_key]['time_windows'][completeness]['precision']

    def getPrecisionErrorForTimeWindow(self, device_key, completeness):
        return self.state[device_key]['time_windows'][completeness]['precision_error']

    def getMaxRelativeArrivalTime(self, device_key):
        return self.state[device_key]['max_relative_arrival_time']

    def getAvgRelativeArrivalTime(self, device_key):
        return self.state[device_key]['avg_relative_arrival_time']


    def addRelativeArrivalTimes(self, device_key, rats):
        self.state[device_key]['relative_arrival_times'] = rats

    def addPastWindow(self, device_key, past_window):
        self.state[device_key]['past_windows'].append(past_window)

    def addTimeWindow(self, device_key, completeness, time_window):
        if not completeness in self.state[device_key]['time_windows'].keys():
            self.state[device_key]['time_windows'][completeness] = dict()
            self.state[device_key]['time_windows'][completeness]['prediction'] = [time_window]
            #self.state[device_key]['time_windows'][completeness]['precision'] = None
            #self.state[device_key]['time_windows'][completeness]['accuracy'] = None
        else:
            self.state[device_key]['time_windows'][completeness]['prediction'].append(time_window)

    def addCompleteness(self, device_key, time_window, completeness):
        if not time_window in self.state[device_key]['completeness'].keys():
            self.state[device_key]['completeness'][time_window] = dict()
            self.state[device_key]['completeness'][time_window]['prediction'] = [completeness]
            self.state[device_key]['completeness'][time_window]['actual_completeness'] = []
            self.state[device_key]['completeness'][time_window]['prediction_error'] = []
        else:
            self.state[device_key]['completeness'][time_window]['prediction'].append(completeness)

    def addMaxRelativeArrivalTime(self, device_key, max):
        self.state[device_key]['max_relative_arrival_time'] = max

    def addAvgRelativeArrivalTime(self, device_key, avg):
        self.state[device_key]['avg_relative_arrival_time'] = avg


    def addAlpha(self, device_key, alpha):
        self.state[device_key]['alpha'] = alpha

    def addBeta(self, device_key, beta):
        self.state[device_key]['beta'] = beta

    # def addK(self, device_key, K):
    #     self.state[device_key]['K'] = K

    def addSamplingRate(self, device_key, sampling_rate):
        self.state[device_key]['sampling_rate'] = sampling_rate
