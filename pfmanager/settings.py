import dataclasses
from dataclasses import field


@dataclasses.dataclass
class ManagerSettings:
    """
        remote - if using remote adb server
        max_devices - max number of devices, 0 - unlimited
    """

    ip: str = '127.0.0.1'
    port: int = 5037
    remote: bool = False
    max_devices: int = 0
    deny: bool = True # block other connections
    nameservers: list[str] = field(default_factory=lambda: ['1.1.1.1', '8.8.8.8'])
