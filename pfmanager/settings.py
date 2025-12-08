import dataclasses


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