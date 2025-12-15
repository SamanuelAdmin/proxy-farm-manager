from pfmanager.settings import ManagerSettings


def main() -> None:
    # configs
    settings = ManagerSettings(
        inner_interfaces=['enp4s0']
    )


if __name__ == '__main__': main()