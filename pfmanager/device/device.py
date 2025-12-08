import adbutils

from .idevice import IDevice


class Device(IDevice):
    def __init__(self, serial: str, adbDevice: adbutils.AdbDevice):
        self._serial = serial
        self.__adb: adb.AdbDevice = adbDevice

    def checkConnection(self, timeout: int=1000) -> int:
        commandResult: str = self.__adb.shell(f'ping -c 1 -W {timeout} example.com')
        if 'Network is unreachable' in commandResult: return 0

        return 1