import functools
from curses import wrapper
from typing import Callable
import adbutils
import re

from .idevice import IDevice


_checkConnectionPatters: list[re.Pattern] = [
        re.compile(r"network is unreachable", re.IGNORECASE),
    ]


class Device(IDevice):
    def __init__(self, serial: str, adbDevice: adbutils.AdbDevice):
        self._serial = serial
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
    def checkConnection(self, host: str="1.1.1.1", timeout: int=1000) -> int:
        commandResult: str = self.__adb.shell(f'ping -c 1 -W {timeout} {host}')

        if any([ pattern.search(commandResult) for pattern in _checkConnectionPatters ]):
            print(f'[Warning] Device {self._serial} has no internet connection.')
            return 0

        return 1