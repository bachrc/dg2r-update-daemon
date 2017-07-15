from threading import Thread
from time import sleep

from update_daemon import STATE


class Update(Thread):
    def __init__(self, state):
        super().__init__()
        self.state = state

    def run(self):
        while self.state.queue[-1] == STATE.DISPLAYING:
            sleep(1)

        sleep(6)
        self.state.put(STATE.SUCCESS)
        print("J'ai fini, catin.")
