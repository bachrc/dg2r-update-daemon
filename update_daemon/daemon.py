import sys
import argparse

from pathlib import Path

from update_daemon.data import UpdateObject


def path_to_update(path):
    path = Path(path)

    if not path.is_dir():
        raise argparse.ArgumentTypeError("The update source isn't a folder, please check your udev rules or your "
                                         "USB key permissions.")

    return path


def scan():
    parser = argparse.ArgumentParser(description="Scans given directory in order to change current Armadillo app")
    parser.add_argument('path', nargs=1, help="The mounted usb key folder path", type=path_to_update)

    args = parser.parse_args()

    path = args.path

    path_to_file = Path(path / "UPDATE.dg2r")
    if path_to_file.is_file():
        try:
            update = UpdateObject.load(path_to_file)

            

        except Exception as e:





if __name__ == '__main__':
    scan()
