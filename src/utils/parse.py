import os
import numpy as np
from src.utils.stats import *
import json

def parseStaticOracleTimeouts(fn):
    result = dict()
    file = os.path.join(os.getcwd(), 'Static_Oracle_Configuration')
    filename = os.path.join(file, fn)
    with open(os.path.join(file, filename)) as f:
        start = False
        for line in f:
            if not start:
                start = True
            else:
                parsed_line = line.split(',')
                device  = parsed_line[0]
                constraint = parsed_line[1]
                timeout = parsed_line[2]
                mer = parsed_line[3]
                distance = parsed_line[4]
                bc = parsed_line[5].rstrip()
                if not device in result.keys():
                    result[device] = dict()
                if not constraint in result[device].keys():
                    result[device][float(constraint)] = dict()
                result[device][float(constraint)]['timeout'] = timeout
                result[device][float(constraint)]['mer'] = mer
                result[device][float(constraint)]['prediction_latency'] = distance
                result[device][float(constraint)]['below_constraint'] = bc
    return result

def parseDSPTimeouts(fn, setName=None):
    device_to_sr = {
        '1010/9000|fd34::0017:0d00:0030:dabe': 835,
        '9903/9904/2|fd34::0017:0d00:0030:dabe': 111.3,
        '1010/9000|fd34::0017:0d00:0030:dadf': 820,
        '3302/5500|fd34::0017:0d00:0030:dadf': 109.25,
        '1010/9000|fd34::0017:0d00:0030:dfe8': 814,
        '9803/9805|fd34::0017:0d00:0030:dfe8': 9,
        '1010/9000|fd34::0017:0d00:0030:e0fe': 856,
        '8040/8042|fd34::0017:0d00:0030:e0fe': 57,
        '1010/9000|fd34::0017:0d00:0030:e3a0': 809,
        '3303/5702|fd34::0017:0d00:0030:e3a0': 107.8,
        '1010/9000|fd34::0017:0d00:0030:e3ca': 823,
        '9803/9805|fd34::0017:0d00:0030:e3ca': 55,
        '1010/9000|fd34::0017:0d00:0030:e69f': 835.5,
        '3302/5500|fd34::0017:0d00:0030:e69f': 111.25,
        '1010/9000|fd34::0017:0d00:0030:e6a6': 822,
        '3302/5500|fd34::0017:0d00:0030:e6a6': 109,
        '1010/9000|fd34::0017:0d00:0030:e72d': 818.5,
        '3303/5702|fd34::0017:0d00:0030:e72d': 109.2,
        '1010/9000|fd34::0017:0d00:0030:e947': 814.5,
        '3303/5702|fd34::0017:0d00:0030:e947': 54.3,
        '1010/9000|fd34::0017:0d00:0030:e95e': 834.5,
        '9803/9805|fd34::0017:0d00:0030:e95e': 9
    }
    device_to_sr_dec = {
        '1010/9000|fd34::0017:0d00:0030:dabe': 222.7,
        '9903/9904/2|fd34::0017:0d00:0030:dabe': 222.7,
        '1010/9000|fd34::0017:0d00:0030:dadf': 218.655,
        '3302/5500|fd34::0017:0d00:0030:dadf': 218.655,
        '1010/9000|fd34::0017:0d00:0030:dfe8': 217.2,
        '9803/9805|fd34::0017:0d00:0030:dfe8': 217.2,
        '1010/9000|fd34::0017:0d00:0030:e0fe': 228.5,
        '8040/8042|fd34::0017:0d00:0030:e0fe': 228.5,
        '1010/9000|fd34::0017:0d00:0030:e3a0': 216,
        '3303/5702|fd34::0017:0d00:0030:e3a0': 216,
        '1010/9000|fd34::0017:0d00:0030:e3ca': 220.1,
        '9803/9805|fd34::0017:0d00:0030:e3ca': 220.1,
        '1010/9000|fd34::0017:0d00:0030:e69f': 222.8,
        '3302/5500|fd34::0017:0d00:0030:e69f': 222.8,
        '1010/9000|fd34::0017:0d00:0030:e6a6': 219.1,
        '3302/5500|fd34::0017:0d00:0030:e6a6': 219.1,
        '1010/9000|fd34::0017:0d00:0030:e72d': 218.08,
        '3303/5702|fd34::0017:0d00:0030:e72d': 218.08,
        '1010/9000|fd34::0017:0d00:0030:e947': 217.21,
        '3303/5702|fd34::0017:0d00:0030:e947': 217.21,
        '1010/9000|fd34::0017:0d00:0030:e95e': 223.4,
        '9803/9805|fd34::0017:0d00:0030:e95e': 223.4
    }
    device_to_sr_inc = {
        '1010/9000|fd34::0017:0d00:0030:dabe': 55.7,
        '9903/9904/2|fd34::0017:0d00:0030:dabe': 55.7,
        '1010/9000|fd34::0017:0d00:0030:dadf': 54.67,
        '3302/5500|fd34::0017:0d00:0030:dadf': 54.67,
        '1010/9000|fd34::0017:0d00:0030:dfe8': 54.3,
        '9803/9805|fd34::0017:0d00:0030:dfe8': 54.29,
        '1010/9000|fd34::0017:0d00:0030:e0fe': 57.14,
        '8040/8042|fd34::0017:0d00:0030:e0fe': 57.14,
        '1010/9000|fd34::0017:0d00:0030:e3a0': 53.96,
        '3303/5702|fd34::0017:0d00:0030:e3a0': 53.96,
        '1010/9000|fd34::0017:0d00:0030:e3ca': 55.08,
        '9803/9805|fd34::0017:0d00:0030:e3ca': 55.08,
        '1010/9000|fd34::0017:0d00:0030:e69f': 55.71,
        '3302/5500|fd34::0017:0d00:0030:e69f': 55.71,
        '1010/9000|fd34::0017:0d00:0030:e6a6': 54.81,
        '3302/5500|fd34::0017:0d00:0030:e6a6': 54.81,
        '1010/9000|fd34::0017:0d00:0030:e72d': 54.59,
        '3303/5702|fd34::0017:0d00:0030:e72d': 54.4,
        '1010/9000|fd34::0017:0d00:0030:e947': 54.4,
        '3303/5702|fd34::0017:0d00:0030:e947': 54.3,
        '1010/9000|fd34::0017:0d00:0030:e95e': 54.4,
        '9803/9805|fd34::0017:0d00:0030:e95e': 56
    }
    # print('Parsing Sampling Rates...')
    result = dict()
    #sr = parseDataSet(fn)
    #sr_to_sr = dict()
    #for sampling_rate in sr.keys():
    #    print('sr[sampling_rate', sr[sampling_rate])
    #    sr_to_sr[sampling_rate] = math.floor(np.mean(np.array(sr[sampling_rate])))
    #print('sr_to_sr', sr_to_sr)
    current_directory = os.path.join(os.getcwd(), 'data_sets')
    # device_to_sr = data["initial_sampling_periods"]
    with open(os.path.join(current_directory, fn)) as f:
        start = True
        for line in f:
            if not start:
                parsed_line = line.split(';')
                device_info = parsed_line[0][parsed_line[0].index('{') + 1:parsed_line[0].index('}')]
                device_info_parsed = device_info.split(',')
                mote = device_info_parsed[0][6:]
                peripheral = device_info_parsed[1][13:]
                sampling_rate = device_info_parsed[2][16:]
                # timestamp = parsed_line[1].split('+')[0]
                key = peripheral + '|' + mote
                # rat = parsed_line[2].rstrip()
                # print('sampling_rate:', sampling_rate)

                if key not in result.keys():
                    result[key] = dict()
                    for cc in np.linspace(0.1,1,10):
                        result[key][round(cc,1)] = dict()
                        if setName == 'inc':
                            result[key][round(cc, 1)]['timeout'] = float(device_to_sr_inc[key]) * 2
                        elif setName == 'dec':
                            result[key][round(cc, 1)]['timeout'] = float(device_to_sr_dec[key]) * 2
                        else:
                            result[key][round(cc, 1)]['timeout'] = float(device_to_sr[key]) * 2

            else:
                start = False
    return result

def parseSPNDTimeouts(fn, lats_fn, setName = None):
    device_to_sr = {
        '1010/9000|fd34::0017:0d00:0030:dabe': 835,
        '9903/9904/2|fd34::0017:0d00:0030:dabe': 111.3,
        '1010/9000|fd34::0017:0d00:0030:dadf': 820,
        '3302/5500|fd34::0017:0d00:0030:dadf': 109.25,
        '1010/9000|fd34::0017:0d00:0030:dfe8': 814,
        '9803/9805|fd34::0017:0d00:0030:dfe8': 9,
        '1010/9000|fd34::0017:0d00:0030:e0fe': 856,
        '8040/8042|fd34::0017:0d00:0030:e0fe': 57,
        '1010/9000|fd34::0017:0d00:0030:e3a0': 809,
        '3303/5702|fd34::0017:0d00:0030:e3a0': 107.8,
        '1010/9000|fd34::0017:0d00:0030:e3ca': 823,
        '9803/9805|fd34::0017:0d00:0030:e3ca': 55,
        '1010/9000|fd34::0017:0d00:0030:e69f': 835.5,
        '3302/5500|fd34::0017:0d00:0030:e69f': 111.25,
        '1010/9000|fd34::0017:0d00:0030:e6a6': 822,
        '3302/5500|fd34::0017:0d00:0030:e6a6': 109,
        '1010/9000|fd34::0017:0d00:0030:e72d': 818.5,
        '3303/5702|fd34::0017:0d00:0030:e72d': 109.2,
        '1010/9000|fd34::0017:0d00:0030:e947': 814.5,
        '3303/5702|fd34::0017:0d00:0030:e947': 54.3,
        '1010/9000|fd34::0017:0d00:0030:e95e': 834.5,
        '9803/9805|fd34::0017:0d00:0030:e95e': 9
    }
    device_to_sr_dec = {
        '1010/9000|fd34::0017:0d00:0030:dabe': 222.7,
        '9903/9904/2|fd34::0017:0d00:0030:dabe': 222.7,
        '1010/9000|fd34::0017:0d00:0030:dadf': 218.655,
        '3302/5500|fd34::0017:0d00:0030:dadf': 218.655,
        '1010/9000|fd34::0017:0d00:0030:dfe8': 217.2,
        '9803/9805|fd34::0017:0d00:0030:dfe8': 217.2,
        '1010/9000|fd34::0017:0d00:0030:e0fe': 228.5,
        '8040/8042|fd34::0017:0d00:0030:e0fe': 228.5,
        '1010/9000|fd34::0017:0d00:0030:e3a0': 216,
        '3303/5702|fd34::0017:0d00:0030:e3a0': 216,
        '1010/9000|fd34::0017:0d00:0030:e3ca': 220.1,
        '9803/9805|fd34::0017:0d00:0030:e3ca': 220.1,
        '1010/9000|fd34::0017:0d00:0030:e69f': 222.8,
        '3302/5500|fd34::0017:0d00:0030:e69f': 222.8,
        '1010/9000|fd34::0017:0d00:0030:e6a6': 219.1,
        '3302/5500|fd34::0017:0d00:0030:e6a6': 219.1,
        '1010/9000|fd34::0017:0d00:0030:e72d': 218.08,
        '3303/5702|fd34::0017:0d00:0030:e72d': 218.08,
        '1010/9000|fd34::0017:0d00:0030:e947': 217.21,
        '3303/5702|fd34::0017:0d00:0030:e947': 217.21,
        '1010/9000|fd34::0017:0d00:0030:e95e': 223.4,
        '9803/9805|fd34::0017:0d00:0030:e95e': 223.4
    }
    device_to_sr_inc = {
        '1010/9000|fd34::0017:0d00:0030:dabe': 55.7,
        '9903/9904/2|fd34::0017:0d00:0030:dabe': 55.7,
        '1010/9000|fd34::0017:0d00:0030:dadf': 54.67,
        '3302/5500|fd34::0017:0d00:0030:dadf': 54.67,
        '1010/9000|fd34::0017:0d00:0030:dfe8': 54.3,
        '9803/9805|fd34::0017:0d00:0030:dfe8': 54.29,
        '1010/9000|fd34::0017:0d00:0030:e0fe': 57.14,
        '8040/8042|fd34::0017:0d00:0030:e0fe': 57.14,
        '1010/9000|fd34::0017:0d00:0030:e3a0': 53.96,
        '3303/5702|fd34::0017:0d00:0030:e3a0': 53.96,
        '1010/9000|fd34::0017:0d00:0030:e3ca': 55.08,
        '9803/9805|fd34::0017:0d00:0030:e3ca': 55.08,
        '1010/9000|fd34::0017:0d00:0030:e69f': 55.71,
        '3302/5500|fd34::0017:0d00:0030:e69f': 55.71,
        '1010/9000|fd34::0017:0d00:0030:e6a6': 54.81,
        '3302/5500|fd34::0017:0d00:0030:e6a6': 54.81,
        '1010/9000|fd34::0017:0d00:0030:e72d': 54.59,
        '3303/5702|fd34::0017:0d00:0030:e72d': 54.4,
        '1010/9000|fd34::0017:0d00:0030:e947': 54.4,
        '3303/5702|fd34::0017:0d00:0030:e947': 54.3,
        '1010/9000|fd34::0017:0d00:0030:e95e': 54.4,
        '9803/9805|fd34::0017:0d00:0030:e95e': 56
    }
    # print('Parsing Sampling Rates...')
    result = dict()
    #current_directory = os.path.join(os.getcwd(), 'data_sets_final')
    device_to_latencies = parseLatencies(lats_fn)
    #sr = parseDataSet2(fn)
    #sr_to_sr = dict()
    #for sampling_rate in sr.keys():
    #    print('sr[sampling_rate', sr[sampling_rate])
    #    sr_to_sr[sampling_rate] = math.floor(np.mean(np.array(sr[sampling_rate])))
    current_directory = os.path.join(os.getcwd(), 'Data Sets')
    current_directory = os.path.join(current_directory, 'data_sets_final')
    with open(os.path.join(current_directory, fn)) as f:
        start = True
        for line in f:
            if not start:
                parsed_line = line.split(';')
                device_info = parsed_line[0][parsed_line[0].index('{') + 1:parsed_line[0].index('}')]
                device_info_parsed = device_info.split(',')
                mote = device_info_parsed[0][6:]
                peripheral = device_info_parsed[1][13:]
                sampling_rate = device_info_parsed[2][16:]
                # timestamp = parsed_line[1].split('+')[0]
                key = peripheral + '|' + mote
                # rat = parsed_line[2].rstrip()
                # print('sampling_rate:', sampling_rate)

                if key not in result.keys():
                    result[key] = dict()
                    for cc in np.linspace(0.1,1,10):
                        result[key][round(cc,1)] = dict()
                        lats = []
                        for lat in device_to_latencies[key]:
                            lats.append(float(lat[0]))
                        #result[key][round(cc,1)]['timeout'] = float(sr_to_sr[sampling_rate]) + round(np.mean(np.array(lats)),3)
                        if setName == 'inc':
                            print('inc')
                            result[key][round(cc, 1)]['timeout'] = float(device_to_sr_inc[key]) + round(
                                np.mean(np.array(lats)), 3)
                        elif setName == 'dec':
                            print('dec')
                            result[key][round(cc, 1)]['timeout'] = float(device_to_sr_dec[key]) + round(
                                np.mean(np.array(lats)), 3)
                        else:
                            result[key][round(cc, 1)]['timeout'] = float(device_to_sr[key]) + round(
                                np.mean(np.array(lats)), 3)
            else:
                start = False

    return result

def parseLatencies(filename, state):
    result = dict()
    # make as argumen
    #filename = os.path.join(file, 'lats_short.csv')
    with open(filename) as f:
        start = True
        for line in f:
            if not start:
               # print('line:', line)
                parsed_line = line.split(';')
                #print('parsed_line[0]', parsed_line[0])
                #print('parsed_line[1]', parsed_line[1])
                #print('parsed_line[2]', parsed_line[2])
                device_info = parsed_line[0][parsed_line[0].index('{') + 1:parsed_line[0].index('}')]
                #print('device_info:', device_info)
                mote = device_info[6:]

                timestamp = parsed_line[1][0:len(parsed_line[1]) - 1]
                avg_latency = parsed_line[2].rstrip()
                avg_latency = avg_latency.replace(',', '')
                device_key = mote.split(',')[1].split(':')[1][1:] + '|' + mote.split(',')[0]
                #print('mote', mote)
                #device_key = prettifyMAC(mote)
                if not device_key in result.keys():
                    state.state[device_key]['lats'] = [(float(avg_latency), timestamp)]
                else:
                    state.state[device_key]['lats'].append((float(avg_latency), timestamp))
            else:
                start = False
    #return result


#########
def prettifyMAC(mac):
    # print('mac', mac)
    result = 'fd34::0017:0d00:00'
    parsed = mac.split('-')
    # print('parsed:', parsed)
    result = result + parsed[5] + ':' + parsed[6].lower() + parsed[7].lower()
    return result



def parseMote(line):
    if (line.index("mote:") != -1):
        parsed_line = line.split('mote: ')
        return parsed_line[1][1:len(parsed_line[1]) - 1]
    return -1

def parseSamplingRates(filename,state):
    #print('Parsing Sampling Rates...')
    result = dict()
    #current_directory = os.path.join(os.getcwd(), 'data_sets')
    with open(filename) as f:
        start = True
        for line in f:
            if not start:
                parsed_line = line.split(';')
                device_info = parsed_line[0][parsed_line[0].index('{') + 1:parsed_line[0].index('}')]
                device_info_parsed = device_info.split(',')
                mote = device_info_parsed[0][6:]
                peripheral = device_info_parsed[1][13:]
                sampling_rate = device_info_parsed[2][16:]
                #timestamp = parsed_line[1].split('+')[0]
                key = peripheral + '|' + mote
                #rat = parsed_line[2].rstrip()
               # print('sampling_rate:', sampling_rate)
                if not key in result.keys():
                    state.addSamplingRate(key, float(sampling_rate))
                    result[key] = float(sampling_rate)
            else:
                start = False
    return result

        # it will look for file in current directory



    # it will look for file in current directory
def parseDataSet(filename, state):
    #print('Parsing Data Set...')
    device_to_rat = dict()
    #current_directory = os.path.join(os.getcwd(), 'Data Sets')
    # print('current dir', current_directory)
    #current_directory = os.path.join(current_directory, 'data_sets_final')
    # print('current dir', current_directory)
    # print('data set', data_set)
    #current_directory = os.path.join(current_directory, data_set)
    # print('current dir', current_directory)
    #fp = os.path.join(current_directory, data_set)
    with open(filename) as f:
        start = True
        for line in f:
            if not start:
                #print('line:', line)
                parsed_line = line.split(';')
                #print('parsed_line', parsed_line)
                #print('parsed_line[0]', parsed_line[0])
                #print('parsed_line[1]', parsed_line[1])
                device_info = parsed_line[0][parsed_line[0].index('{') + 1:parsed_line[0].index('}')]
                device_info_parsed = device_info.split(',')
                mote = device_info_parsed[0][6:]
                peripheral = device_info_parsed[1][13:]
                timestamp = parsed_line[1][0:len(parsed_line[1]) - 1]
                timestamp = timestamp.strip('"')
                #print('timestamp:', timestamp)
                #print('timestamp[1:]', timestamp[1:len(timestamp) - 1])
                key = peripheral + '|' + mote
                rat = parsed_line[2].rstrip()
                rat = float(rat.replace(',',''))
                if key in device_to_rat.keys():
                    device_to_rat[key].append((float(rat), timestamp))
                else:
                    state.registerDevice(key)
                    device_to_rat[key] = [(float(rat), timestamp)]
            else:
                start = False

    for key in device_to_rat.keys():
        device_to_rat[key] = removeOutliers(device_to_rat[key])
        #print('rats to be added:', device_to_rat[key] )
        state.addRelativeArrivalTimes(key, device_to_rat[key])
        #print('rats added:', self.state.state[key]['relative_arrival_times'])

    return device_to_rat


# def parseDataSet(self,data_set):
#     device_to_rat = dict()
#     current_directory = os.path.join(os.getcwd(), 'data_sets')
#     with open(os.path.join(current_directory, data_set)) as f:
#         start = True
#         for line in f:
#             if not start:
#                 print('line:', line)
#                 #parsed_line = line.split(';')
#                 #print('parsed_line[0]', parsed_line[0])
#                 #print('parsed_line[1]', parsed_line[1])
#                 device_info = line[line.index('{') + 1:line.index('}')]
#                 device_info_parsed = device_info.split(',')
#                 mote = device_info_parsed[0][6:]
#                 peripheral = device_info_parsed[1][13:]
#                 timestamp = line.split(',')[len(line.split(',')) - 2]
#                 print('timestamp:', timestamp)
#                 #print('timestamp:', timestamp)
#                 #print('timestamp[1:]', timestamp[1:len(timestamp) - 1])
#                 key = peripheral + '|' + mote
#                 rat = line.split(',')[len(line.split(',')) - 1].rstrip()
#                 print('rat:', rat)
#                 if key in device_to_rat.keys():
#                     device_to_rat[key].append((float(rat), timestamp))
#                 else:
#                     self.state.registerDevice(key)
#                     device_to_rat[key] = [(float(rat), timestamp)]
#             else:
#                 start = False
#     for key in device_to_rat.keys():
#         self.state.addRelativeArrivalTimes(key, device_to_rat[key])
#
#     return device_to_rat

#####