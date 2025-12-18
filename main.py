import pfmanager
from pfmanager.settings import ManagerSettings
from pfmanager import Manager


def main() -> None:
    # configs
    settings = ManagerSettings(inner_interfaces=["enp4s0"])

    pfManager = Manager(settings=settings)
    pfManager.init()

    pfmanager.startProxyServer()


if __name__ == "__main__":
    main()

