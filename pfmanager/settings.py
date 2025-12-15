from dataclasses import dataclass, field



@dataclass
class ProxySettings:
    """
        Settings for proxy server (squid).
    """
    ip: str = '127.0.0.1'
    port: int = 3331
    remote: bool = False
    max_devices: int = 0 # 0 - unlimited
    deny: bool = True # block other connections
    nameservers: list[str] = field(default_factory=lambda: ['1.1.1.1', '8.8.8.8'])
    path_to_squid: str = "/etc/squid/squid.conf",
    service_name = "squid.service"


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

    proxySettings: ProxySettings = ProxySettings()
    adbSettings: AdbSettings = AdbSettings()