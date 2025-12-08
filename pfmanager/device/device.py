import functools
import time
from typing import Callable, Optional
import adbutils
import re

from .idevice import IDevice


_checkConnectionPatters: list[re.Pattern] = [
        re.compile(r"network is unreachable", re.IGNORECASE),
    ]


class Device(IDevice):
    def __init__(self, serial: str, adbDevice: adbutils.AdbDevice):
        self._serial = serial
        self._activates: bool = False
        self._hotspotIp: Optional[str] = None # IP of local interface (from usb tethering)
        self.__adb: adbutils.AdbDevice = adbDevice


    def ifOnline(function: Callable) -> Callable:
        """
            Checks if device is online or not.
            USE IT WITH EVERY DEVICE OPERATION.
        """

        functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            #!TODO Finish this decorator
            # if not self.__adb.isOnline():
            #     raise Exception("Device is not online")

            return function(self, *args, **kwargs)

        return wrapper


    @ifOnline
    def _controlMobileData(self, status: bool) -> None:
        """ Turn on or off mobile data. """
        print(f'[INFO] {self._serial} mobile data turned {"on" if status else "off"}.')
        self.__adb.shell(f'svc data {"enable" if status else "disable"}')

    @ifOnline
    def _controlUsbTethering(self, status: bool) -> None:
        """ Turn on or off usb tethering. """
        print(f'[INFO] {self._serial} usb tethering turned {"on" if status else "off"}.')
        self.__adb.shell(f'svc usb setFunctions {"rndis,adb" if status else "mtp,adb"}')

    @ifOnline
    def _getLocalIp(self, interface: str="rndis0") -> str:
        return self.__adb.shell("ip -o -4 addr show " + interface + " | awk -F '[ /]+' '/inet/ {print $4}'")

    @ifOnline
    def _restart(self):
        """ Restart the physical device. """
        self.__adb.reboot()


    @ifOnline
    def checkConnection(self, host: str="1.1.1.1", timeout: int=1000) -> int:
        self._controlMobileData(True)
        commandResult: str = self.__adb.shell(f'ping -c 1 -W {timeout} {host}')

        if any([ pattern.search(commandResult) for pattern in _checkConnectionPatters ]):
            print(f'[Warning] Device {self._serial} has no internet connection.')
            return 0

        return 1

    def activate(self, delay:int=1):
        """ Activate device as a proxy tunel. """
        self._controlMobileData(True)
        self._controlUsbTethering(True)
        time.sleep(delay)

        self._ACTIVATED = True
        self._hotspotIp = self._getLocalIp()

        print(f'[INFO] {self._serial} set up to interface mode. Device IP: {self._hotspotIp}.')

