from typing import TypeVar, Iterator, Generic
import adbutils
import os

from . import IDevice
from .device import Device
from .proxy_server import ProxyServerConfigurator, ProxyServerController
from .settings import ManagerSettings


T = TypeVar("T", bound=IDevice)


def checkForRootPermissions():
    """ True if user has root permissions. """
    return os.geteuid() == 0


class Manager(Generic[T]):
    """
        Main controller for all devices.
        Template - realization of IDevice, by default - Device.
    """

    def __init__(self, template:type[T]=Device, settings: ManagerSettings=ManagerSettings) -> None:
        self.__template: type[T] = template
        self.__settings: ManagerSettings = settings

        self.__ProxyServerConfigurator: ProxyServerConfigurator = ProxyServerConfigurator(
            self.__settings.proxySettings
        )
        self.__ProxyServerController: ProxyServerController = ProxyServerController(
            self.__ProxyServerConfigurator
        )
        self.__adbManager = adbutils.AdbClient(
            host=settings.adbSettings.ip, port=settings.adbSettings.port
        )

        self.__devices: dict[str, T] = {
            serial: device for serial, device in self.iterDevices
        }
        self.__connected: dict[str, T] = {
            serial: device for serial, device in self.iterConnectedDevices
        }


    @property
    def processedDevices(self) -> dict[str, T]:
        """ All devices, which have been processed. """
        return self.__devices


    @property
    def iterDevices(self) -> Iterator[tuple[str, T]]:
        """
            Creating list of all devices using IDevice class,
            which you put in template variable. By default - Device class.
            :return Devices, one by one (generator), created by template class
        """

        for dev in self.__adbManager.device_list():
            yield dev.serial, self.__template(dev.serial, dev)


    @property
    def iterConnectedDevices(self) -> Iterator[tuple[str, T]]:
        """
        Check for connected to internet devices.
        :return: Devices, one by one (generator)
        """

        if not self.__devices:
            raise Exception('Cannot check connected devices - device list is empty.')

        for serial, device in self.__devices.items():
            if device.checkConnection() > 0:
                yield serial, device


    def startProxyServer(self):
        pass