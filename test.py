from lpd8.pgm_chg import Pgm_Chg

class Test:

    def __init__(self):
        self._running = True

    def is_running(self):
        return self._running

    def stop(self):
        self._running = False

    def ctrl_value(self, data):
        print('CTRL : ' + str(data))

    def note_on_value(self, data):
        print('NOTE ON : ' + str(data))

    def note_off_value(self, data):
        print('NOTE OFF : ' + str(data))

    def pgm_change(self, data):
        print('PGM CHG : ' + str(data))
        if data[1] == Pgm_Chg.PGM_CHG_4:
            self._running = False
