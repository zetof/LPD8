from lpd8.programs import Programs

class Pad:

    NO_MODE = 0
    SWITCH_MODE = 1
    PUSH_MODE = 2
    PAD_MODE = 4
    BLINK_MODE = 8

    OFF = 0
    ON = 1
    BLINK = 2

    def __init__(self, mode=PAD_MODE):
        self.set_mode(mode)
        self._state = self.OFF

    def _get_action(self):
        if self._mode > self.BLINK_MODE:
            return self._mode - self.BLINK_MODE
        else:
            return self._mode

    def get_state(self):
        state = self.OFF
        if self._mode >= self.BLINK_MODE:
            if self._mode - self.BLINK_MODE == self.SWITCH_MODE and self._state == self.ON:
                state = self.ON
            else:
                state = self.BLINK
        elif self._mode == self.SWITCH_MODE and self._state == self.ON:
            state = self.ON
        return state

    def set_mode(self, mode):
        self._mode = mode

    def note_on(self, velocity):
        action = self._get_action()
        if action == self.SWITCH_MODE:
            if self._state == self.ON:
                self._state = self.OFF
            else:
                self._state = self.ON
            return self._state
        elif action == self.PUSH_MODE:
            return self.ON
        elif action == self.PAD_MODE:
            return velocity
        else:
            return None

    def note_off(self):
        action = self._get_action()
        if action == self.SWITCH_MODE:
            return self._state
        elif action == self.PUSH_MODE or action == self.PAD_MODE:
            return self.OFF
        else:
            return None


class Pads:

    PAD_1 = 60
    PAD_2 = 62
    PAD_3 = 64
    PAD_4 = 65
    PAD_5 = 67
    PAD_6 = 69
    PAD_7 = 71
    PAD_8 = 72

    ALL_PADS = [PAD_1, PAD_2, PAD_3, PAD_4, PAD_5, PAD_6, PAD_7, PAD_8]
    PAD_MAX = len(ALL_PADS)

    _pad_index = {
        PAD_1: 1,
        PAD_2: 2,
        PAD_3: 3,
        PAD_4: 4,
        PAD_5: 5,
        PAD_6: 6,
        PAD_7: 7,
        PAD_8: 8
    }

    def __init__(self, programs=Programs.PGM_MAX, pads=PAD_MAX):
        self._pads = []
        for program in range(programs + 1):
            self._pads.append([])
            for pad in range(pads + 1):
                self._pads[program].append(Pad())

    def set_mode(self, program, pad, mode):
        self._pads[program][self._pad_index[pad]].set_mode(mode)

    def note_on(self, program, pad, velocity):
        return self._pads[program][self._pad_index[pad]].note_on(velocity)

    def note_off(self, program, pad):
        return self._pads[program][self._pad_index[pad]].note_off()

    def get_state(self, program, pad):
        return self._pads[program][self._pad_index[pad]].get_state()
