from functools import wraps
from typing import TypeVar, Iterator, Generic, Callable
import adbutils
import os
from abc import ABC, abstractmethod

from . import IDevice, settings
from .device import Device
from .networks_manager import NetworkInterface, NetworksManager, BridgeInterface
from .proxy_interface import ProxyInterface
from .proxy_server import ProxyServerConfigurator, ProxyServerController
from .settings import ManagerSettings


T = TypeVar("T", bound=IDevice)


def checkForRootPermissions():
    """ True if user has root permissions. """
    return os.geteuid() == 0


class ILoadable(ABC):
    @property
    @abstractmethod
    def loaded(self) -> bool: ...

def after_load(function: Callable) -> Callable:
    """
        Checker for loaded
    """

    @wraps(function)
    def wrapper(self: ILoadable, *args, **kwargs):
        if not self.loaded: raise Exception('Cannot do an action before loading!')
        return function(self, *args, **kwargs)

    return wrapper



class Manager(Generic[T], ILoadable):
    """
        Main controller for all devices.
        Template - realization of IDevice, by default - Device.
    """

    def __init__(self, settings: ManagerSettings=ManagerSettings, template:type[T]=Device) -> None:
        self.__template: type[T] = template
        self.__settings: ManagerSettings = settings

        self.__LOADED: bool = False

        self.__networkManager: NetworksManager = NetworksManager()

        self.__proxyServerConfigurator: ProxyServerConfigurator = ProxyServerConfigurator(
            self.__settings.proxySettings
        )
        self.__proxyServerController: ProxyServerController = ProxyServerController(
            self.__proxyServerConfigurator
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
    def loaded(self) -> bool: return self.__LOADED

    @property
    def processedDevices(self) -> dict[str, T]:
        """ All devices, which have been processed. """
        return self.__devices


    @property
    def iterDevices(self) -> Iterator[tuple[str, T]]:
        """jcd4@1!7_12
            Creating list of all devices using IDevice class,
            which you put in template variable. By default - Device class.
            :return: Devices, one by one (generator), created by template class
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


    def init(self) -> bool:
        """
            Init has few important pasts:
            1) getting devices and wrappers for them (proxyInterfaces)
            2) activate proxy interfaces, catching physic interfaces
            3) configure proxy server by gotten proxy interfaces
            4) configure the inner interfaces, bridge
            5) create (or update) 3proxy systemd unit

            And then system will be ready to start
        """

        interfaces = self.__networkManager.getAllInterfaces()

        # getting devices and wrappers for them (proxyInterfaces)
        proxyInterfaces = [ProxyInterface(dev) for serial, dev in self.__connected.items() ]

        # activate proxy interfaces, catching physic interfaces
        for piface in proxyInterfaces: piface.activate()

        # configure proxy server by gotten proxy interfaces
        self.__proxyServerConfigurator.config( [piface.networkData for piface in proxyInterfaces] )

        # configure the inner interfaces, bridge
        bridgeData: BridgeInterface = self.__networkManager.createBridge(
            list( filter( lambda x: x.name in self.__settings.inner_interfaces, interfaces ) ),
            name=self.__settings.bridge_name
        )

        # creating systemd unit
        self.__proxyServerConfigurator.createUnit()
        self.__proxyServerController.reload()

        self.__LOADED = True
        return True


    @after_load
    def startProxyServer(self):
        self.__proxyServerController.start()

    @after_load
    def stopProxyServer(self):
        self.__proxyServerController.stop()

