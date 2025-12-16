import os
from dataclasses import dataclass, field



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')


@dataclass
class ProxySettings:
    """
        Settings for proxy server (squid).
    """
    ip: str = '127.0.0.1'
    start_port: int = 1080
    username: str = 'admin'
    password: str = 'password'
    max_devices: int = 0 # 0 - unlimited
    nameservers: list[str] = field(default_factory=lambda: ['1.1.1.1', '8.8.8.8'])
    path_to_file: str = "/usr/bin/3proxy"
    path_to_configs: str = os.path.join(CONFIGS_DIR, '3proxy.cfg'),
    service_name: str = "3proxy.service",


@dataclass
class AdbSettings:
    """
        Settings for connection to adb server.
    """
    ip: str = '127.0.0.1'
    port: int = 5037


@dataclass
class ManagerSettings:
    """
        remote - if using remote adb server
        max_devices - max number of devices, 0 - unlimited
    """

    inner_interfaces: list[str] = field(default_factory=list)
    bridge_name: str = 'proxy-bridge'

    proxySettings: ProxySettings = field(default=ProxySettings())
    adbSettings: AdbSettings = field(default=AdbSettings())