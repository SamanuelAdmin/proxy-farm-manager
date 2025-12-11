import dbus
from dataclasses import dataclass



@dataclass
class NetworkInterface:
    name: str
    ip_address: str


class NetworksManager:
    """
        DBUS API to the Linux networks manager.
        Singleton for only 1 connection in one period of time.
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance


    def __init__(self, name: str="org.freedesktop.NetworkManager"):
        self.__name = name # dbus service name
        self.__sysbus = dbus.SystemBus()
        self.__networkDbus = self.__sysbus.get_object(self.__name, '/org/freedesktop/NetworkManager')
        self.__networkDbusInterface = dbus.Interface(self.__networkDbus, self.__name)

    def getInterfaceData(self, deviceObject) -> NetworkInterface:
        interfaceName: dbus.String = deviceObject.Get(
            'org.freedesktop.NetworkManager.Device', 'Interface',
            dbus_interface=dbus.PROPERTIES_IFACE
        )

        ip4ConfigPath: dbus.ObjectPath = deviceObject.Get(
            'org.freedesktop.NetworkManager.Device', 'Ip4Config',
            dbus_interface=dbus.PROPERTIES_IFACE
        )

        ip4Config = self.__sysbus.get_object(self.__name, str(ip4ConfigPath))
        ip4Addr: dbus.String = ip4Config.Get(
            'org.freedesktop.NetworkManager.IP4Config', 'AddressData', dbus_interface=dbus.PROPERTIES_IFACE
        )[0].get('address')

        return NetworkInterface(
            name=str(interfaceName),
            ip_address=str(ip4Addr),
        )


    def getAllInterfaces(self) -> list[NetworkInterface]:
        interfaces: list[NetworkInterface] = []

        for devicePath in self.__networkDbusInterface.GetAllDevices():
            deviceObject = self.__sysbus.get_object(self.__name, str(devicePath))
            interfaces.append( self.getInterfaceData(deviceObject) )

        return interfaces



if __name__ == '__main__':
    nm = NetworksManager()
    print(nm.getAllInterfaces())