from adbutils import adb

from .idevice import IDevice


class Device(IDevice):
    def __init__(self, serial):
        self._serial = serial
        self.__adb: adb.AdbDevice = adb.device(serial)

    def checkConnection(self, timeout: int=1000) -> int:
        commandResult: str = self.__adb.shell(f'ping -c 1 -W {timeout} example.com')
        if 'Network is unreachable' in commandResult: return 0

        return 1