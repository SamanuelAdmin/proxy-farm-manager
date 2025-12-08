import functools
from curses import wrapper
from typing import Callable
import adbutils

from .idevice import IDevice


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
    def checkConnection(self, timeout: int=1000) -> int:
        commandResult: str = self.__adb.shell(f'ping -c 1 -W {timeout} example.com')
        print(commandResult)
        if 'Network is unreachable' in commandResult: return 0

        return 1