"""
Manager for the Squid proxy server.
Configurator and dbus controller.
"""

import ipaddress
import os
from typing import Any

import dbus
import shutil

from . import settings
from .networks_manager import NetworkInterface
from .settings import ProxySettings
from .configs.unit_creator import PROXY_UNIT


class ProxyServerConfigurator:
    """
        Configurator for safe and flexible configs.
    """

    def __init__(self, settings: ProxySettings):
        self.__settings = settings
        self.__pathToConfigs: str = settings.path_to_configs
        self.__pathToBackup: str = self.__pathToConfigs + ".back"

    @property
    def service_name(self): return self.__settings.service_name


    def backup(self) -> None:
        if os.path.exists(self.__pathToConfigs):
            shutil.copyfile(self.__pathToConfigs, self.__pathToBackup)


    def restore(self) -> None:
        shutil.copyfile(self.__pathToBackup, self.__pathToConfigs)


    def createUnit(self, defaultPath: str="/usr/lib/systemd/system/") -> None:
        unitData: str = PROXY_UNIT(self.__settings.path_to_file, self.__pathToConfigs)

        with open(os.path.join(defaultPath, self.__settings.service_name), "w") as f:
            f.write(unitData)


    def config(self, interfaces: list[NetworkInterface]) -> dict[str, NetworkInterface]:
        """
            Create configs for 3proxy proxy server and save it to path_to_configs.
            Returns table of processed interfaces, key - port of the proxy server,
            value - NetworkInterface.
        """

        configs: str = ""  # config file content

        configs += "daemon\n"
        configs += "auth none\n"
        configs += "\n"

        result: dict[str, NetworkInterface] = {}

        for index in range(len(interfaces)):
            interface = interfaces[index]
            port = self.__settings.start_port + index

            configs += f"socks -p{port} -e{interface.interface.ip}\n"
            result[port] = interface

        self.backup()
        with open(self.__pathToConfigs, "w") as config:
            config.write(configs)

        return result




class ProxyServerController:
    def __init__(self, configurator: ProxyServerConfigurator):
        self.__configurator = configurator

        # dbus usage
        self.__sysbus = dbus.SystemBus()
        # systemd connector
        self.__systemd1 = self.__sysbus.get_object(
            'org.freedesktop.systemd1', '/org/freedesktop/systemd1'
        )
        self.__systemdManager = dbus.Interface(self.__systemd1, 'org.freedesktop.systemd1.Manager')


    def start(self):
        self.__systemdManager.StartUnit(self.__configurator.service_name, "replace")
        return True

    def stop(self):
        self.__systemdManager.StopUnit(self.__configurator.service_name, "replace")
        return True

    def reload(self):
        """ Reload unit files in daemon-mode """
        self.__systemdManager.Reload()
