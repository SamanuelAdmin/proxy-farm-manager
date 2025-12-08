from typing import TypeVar, Iterator, Generic
import adbutils

from . import IDevice
from .device import Device
from .settings import ManagerSettings


T = TypeVar("T", bound=IDevice)


class Manager(Generic[T]):
    """
        Main controller for all devices.
        Template - realization of IDevice, by default - Device.
    """

    def __init__(self, template:type[T]=Device, settings: ManagerSettings=ManagerSettings) -> None:
        self.__template: type[T] = template
        self.__settings: ManagerSettings = settings
        self.__adbManager = adbutils.AdbClient(host=settings.ip, port=settings.port)

        self.__devices: dict[str, T] = {
            serial: device for serial, device in self.iterDevices()
        }
        self.__connected: dict[str, T] = {
            serial: device for serial, device in self.iterConnectedDevices()
        }


    @property
    def devices(self) -> dict[str, T]:
        return self.__connected


    def iterDevices(self) -> Iterator[tuple[str, T]]:
        """
            Creating list of all devices using IDevice class,
            which you put in template variable. By default - Device class.
            :return Devices, one by one (generator), created by template class
        """

        for serial in self.__adbManager.device_list():
            yield serial, self.__template(serial, self.__adbManager.device(serial))


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

