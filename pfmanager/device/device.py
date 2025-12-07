from .idevice import IDevice


class Device(IDevice):
    def __init__(self, serial):
        self._serial = serial

    def checkConnection(self) -> int:
        return 0