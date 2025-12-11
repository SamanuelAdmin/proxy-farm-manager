from typing import Optional

from pfmanager import IDevice
from pfmanager.networks_manager import NetworkInterface, NetworksManager


class ProxyInterface(IDevice):
    """
        Proxy interface - main info and physical API for the subnetwork.
        Contains network settings, physical interface name, gateway ip for current subnetwork etc.

        IDevice - to proxy public device methods.
    """

    def __init__(self, device: IDevice):
        self._device = device # device - API to control physical adapter
        self._NetworksManager = NetworksManager()
        self._interface: Optional[NetworkInterface] = None

    def interface(self): return self._interface

    def activate(self):
        firstCheck: list[NetworkInterface] = self._NetworksManager.getAllInterfaces()
        self._device.activate()

        secondCheck: list[NetworkInterface] = self._NetworksManager.getAllInterfaces()
        secondCheck.extend(firstCheck)
        self._interface, *_ = secondCheck


    def checkConnection(self, host: str = "", timeout: int = 1000) -> int:
        return self._device.checkConnection(host=host, timeout=timeout)