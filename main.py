from pfmanager import Manager as PFManager
from pfmanager import Device as PFDevice


def main() -> None:
    pfManager = PFManager()
    print(pfManager.devices)

if __name__ == '__main__': main()