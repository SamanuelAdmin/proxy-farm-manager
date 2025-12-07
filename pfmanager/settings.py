import dataclasses


@dataclasses.dataclass
class ManagerSettings:
    """
        remote - if using remote adb server
        max_devices - max number of devices, 0 - unlimited
    """

    remote: bool = False
    max_devices: int = 0