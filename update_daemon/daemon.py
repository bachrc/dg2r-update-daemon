import argparse
from pathlib import Path

from update_daemon import STATE
from update_daemon.data import UpdateObject
from update_daemon.gui.frame import Application
from update_daemon.threads import Update


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
            update_file = UpdateObject.load(path_to_file)
            update_state = STATE.DISPLAYING

            th_update = Update(update_state)
            app = Application(update_state)

            app.mainloop()

        except Exception as e:
            print("rip")




if __name__ == '__main__':
    scan()
