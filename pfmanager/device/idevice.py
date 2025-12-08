from abc import ABC, abstractmethod
from adbutils import adb


class IDevice(ABC):
    """
        Interface for all devices.
        Device obj can control any connected physical device,
        like phone, usb-stick, etc.
    """

    @abstractmethod
    def __init__(self, serial: str, adbDevice: adb.AdbDevice) -> None:
        """ To load device you need a serial addr of this device. """

    @abstractmethod
    def checkConnection(self, timeout: int=1000) -> int:
        """
            To check if device is connected to internet.
            Returns time of response in ms if it is possible.
            If not - returns 1 if connected, 0 - if not.
            :return: Time of response in ms.
        """

