import dbus
from dataclasses import dataclass, field
import ipaddress
from pyroute2 import NDB


@dataclass
class NetworkInterface:
    name: str
    interface: ipaddress.IPv4Interface


@dataclass
class BridgeInterface:
    name: str
    ifacesNames: field(default_factory=list)



class NetworksManager:
    """
        API to the Linux networks manager.
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
        ip4Data: dbus.String = ip4Config.Get(
            'org.freedesktop.NetworkManager.IP4Config', 'AddressData', dbus_interface=dbus.PROPERTIES_IFACE
        )[0].get('address')

        ip4Addr: dbus.String = ip4Data.get('address')
        prefix: dbus.Int32 = ip4Data.get('prefix')

        return NetworkInterface(
            name=str(interfaceName),
            interface=ipaddress.ip_interface(f"{ip4Addr}/{prefix}")
        )


    def getAllInterfaces(self) -> list[NetworkInterface]:
        interfaces: list[NetworkInterface] = []

        for devicePath in self.__networkDbusInterface.GetAllDevices():
            deviceObject = self.__sysbus.get_object(self.__name, str(devicePath))
            interfaces.append( self.getInterfaceData(deviceObject) )

        return interfaces


    def createBridge(self, childrenIfaces: list[NetworkInterface], name="proxy-inner") -> BridgeInterface:
        """
            Create and start a bridge to connect all inner physic interfaces to the logic one.
            Takes all children interfaces from the childrenIfaces, configs for the network from .
        """

        ndb = NDB(log='debug')

        # creating new bridge by "configs"
        with ndb.interfaces.create(ifname=name, kind='bridge') as bridge:

            # all children interfaces down
            for child in childrenIfaces:
                childInterface = ndb.interfaces[child.name]
                childInterface.set(state="down")
                childInterface.commit()

                # adding to the created bridge
                bridge.add_port(child.name)
                # first ip addr in the network diapason
                bridge.add_ip(next(child.interface.network.hosts()))

            # turn bridge up
            bridge.set(
                br_stp_state=1,
                br_group_fwd_mask=0x4000,
                state='up',
            )


        return BridgeInterface(
            name=name, ifacesNames=[chName for chName in childrenIfaces]
        )



if __name__ == '__main__':
    nm = NetworksManager()
    print(nm.getAllInterfaces())