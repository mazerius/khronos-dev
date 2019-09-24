from abc import ABC, abstractmethod


class Stream(ABC):

    @abstractmethod
    def __init__(self, peripheral_id, device_id, state):
        self.peripheral_id = peripheral_id
        self.device_id = device_id
        self.state = state

    # abstract method
    def incrementCollection(self):
        pass