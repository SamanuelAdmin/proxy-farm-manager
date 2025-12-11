"""
Manager for the Squid proxy server.
Configurator and dbus controller.
"""

import dbus


class ProxyConfigurator:
    """
        Configurator for safe and flexible configs.
    """

    def __init__(
            self, path_to_squid: str="/etc/squid/squid.conf",
            service_name="squid.service"
    ):
        self.__pathToConfigs: str = path_to_squid
        self.__serviceName = service_name

    @property
    def service_name(self): return self.__serviceName

    def backup(self): pass

    def restore(self): pass



class ProxyController:
    def __init__(self, configurator: ProxyConfigurator):
        self.__configurator = configurator

        # dbus usage
        self.__sysbus = dbus.SystemBus()
        # systemd connector
        self.__systemd1 = self.__sysbus.get_object(
            'org.freedesktop.systemd1', '/org/freedesktop/systemd1'
        )
        self.__systemdManager = dbus.Interface(self.__systemd1, 'org.freedesktop.systemd1.Manager')


    def start(self) -> bool:
        self.__systemdManager.StartUnit(self.__configurator.service_name, "replace")
        return True

    def stop(self) -> bool:
        self.__systemdManager.StopUnit(self.__configurator.service_name, "replace")
        return True
