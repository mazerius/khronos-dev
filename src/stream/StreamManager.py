# Instantiates a Peripheral object for every peripheral in the network.

from src.stream.StreamFixedK import *


class StreamManager:


    def __init__(self, influxdb_client=None):
        self.streams = list()
        self.influxdb_client = influxdb_client


    def getStreams(self):
        return self.streams


    def createStreamFixedK(self, peripheral_id, device_id, sampling_rate, alpha, beta, lats, state, constraintsToK):
        stream = StreamFixedK(peripheral_id, device_id, sampling_rate, alpha, beta, lats,  state, constraintsToK)
        self.streams.append(stream)


    def getStreamByDeviceID(self, peripheral_id, device_id):
        for stream in self.streams:
            if stream.peripheral_id == peripheral_id and stream.device_id == device_id:
                return stream
        return None


    def streamExists(self, peripheral_id, device_id):
        for peripheral in self.streams:
            if peripheral.peripheral_id == peripheral_id and peripheral.device_id == device_id:
                return True
        return False

    #def computeCompleteness(self, peripheral_id, device_id, time_window):
    #    peripheral = self.getPeripheralById(peripheral_id, device_id)
    #    return peripheral.getCompleteness(time_window)

    #def computeTimeWindow(self, peripheral_id, device_id, safety_percentage):
    #    peripheral = self.getPeripheralById(peripheral_id, device_id)
    #    return peripheral.getTimeWindow(safety_percentage)

    #def trackCompleteness(self, peripheral_id, device_id, timeWindow):
    #    peripheral = self.getPeripheralById(peripheral_id, device_id)
    #    peripheral.trackCompleteness(timeWindow)

    #def trackTimeWindow(self, peripheral_id, device_id, completeness):
    #    peripheral = self.getPeripheralById(peripheral_id, device_id)
    #    peripheral.trackTimeWindow(completeness)