import traceback
from threading import Thread
from time import sleep

from update_daemon import STATE
from update_daemon.data import UpdateObject


class Update(Thread):
    def __init__(self, state, path=None):
        super().__init__()
        self.state = state
        self.path_to_file = path
        print(self.path_to_file)

    def run(self):
        while self.state.queue[-1] == STATE.DISPLAYING:
            sleep(1)

        sleep(2)
        try:
            self.update()
            self.state.put(STATE.SUCCESS)
        except:
            self.state.put(STATE.ERROR)

    def update(self):
        try:
            update_file = UpdateObject.load(self.path_to_file)
            update_file.unzip_folder()

            commands_on_startup = ["@%s" % c.strip() for c in update_file.startup.split('\n') if c.split()]

            to_write = "\n".join(commands_on_startup)

            f = open(update_file.autostart_file, "w")
            f.write(to_write)
            f.close()

        except Exception as e:
            traceback.print_exc()
            raise
