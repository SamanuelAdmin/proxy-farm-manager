from abc import ABC, abstractmethod
import adbutils


class IDevice(ABC):
    """
        Interface for all devices (external API).
        Device obj can control any connected physical device,
        like phone, usb-stick, etc.
    """

    @abstractmethod
    def __init__(self, serial: str, adbDevice: adbutils.AdbDevice) -> None:
        """ To load device you need a serial addr of this device. """

    @abstractmethod
    def checkConnection(self, host:str="", timeout: int=1000) -> int:
        """
            To check if device is connected to internet.
            Returns time of response in ms if it is possible.
            If not - returns 1 if connected, 0 - if not.
            Timeout - timeout of the ping command.
            Host - host for checking the connection. Use Google DNS servers etc.
            :return: Time of response in ms.
        """

    @abstractmethod
    def activate(self):
        """ Activate device as a proxy tunel. """

