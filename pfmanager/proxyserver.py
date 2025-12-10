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

    ):
        self.__pathToConfigs: str = path_to_squid

    def backup(self): pass

    def restore(self): pass



class ProxyController:
    def __init__(self, configurator: ProxyConfigurator):
        self._configurator = configurator

    def start(self): pass

    def stop(self): pass

