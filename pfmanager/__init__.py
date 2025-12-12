import warnings

from .device import IDevice, Device
from .base import Manager, checkForRootPermissions

__version__ = "1.0.0"
__author__ = "Samanuel Admin"

__all__ = [
    'Device',
    'Manager',
]



# checking for root
if not checkForRootPermissions():
    raise Exception("Root permissions required for this package because of using DBUS connections.")
else:
    warnings.warn(f"This package ({__file__}) is using root permissions! Be careful with this.", UserWarning)