from threading import Thread
from time import sleep

from update_daemon import STATE
from update_daemon.data import UpdateObject


class Update(Thread):
    def __init__(self, state, path = None):
        super().__init__()
        self.state = state
        self.path_to_file = path

    def run(self):
        while self.state.queue[-1] == STATE.DISPLAYING:
            sleep(1)

        sleep(6)
        self.state.put(STATE.SUCCESS)

    def update(self):
        try:
            update_file = UpdateObject.load(self.path_to_file)

        except Exception as e:
            print("rip")
