from lpd8.programs import Programs

class Pad:
    """
    Class that defines a single pad
    A pad can have multiple modes and these modes may be combined
    """

    NO_MODE = 0     # Doesn't react to user actions
    SWITCH_MODE = 1 # Switches between 1 and 0 values, both sent at NOTE ON and NOTE OFF events
    PUSH_MODE = 2   # Always sends a 1 at Note ON event and a 0 at NOTE OFF event
    PAD_MODE = 4    # Default mode, acts as a normal pad (sends note value and velocity)
    BLINK_MODE = 8  # May be combined with above modes. Blinks pad at each pad_update call

    OFF = 0
    ON = 1
    BLINK = 2

    def __init__(self, mode=PAD_MODE):
        self.set_mode(mode)
        self._state = self.OFF

    def get_state(self):
        """
        According to the working mode of the pad, returns appropriate value
        :return: The state value
        """
        state = self.OFF
        if self.get_mode(without_blink_mode=False) >= self.BLINK_MODE:
            if self._state == self.ON:
                state = self.ON
            else:
                state = self.BLINK
        elif self._state == self.ON:
            state = self.ON
        return state

    def get_mode(self, without_blink_mode=True):
        """
        Get defined action for this pad. We need this method to get only the action without the blink mode
        :return: mode value without BLINK mode
        """
        if self._mode > self.BLINK_MODE and without_blink_mode:
            return self._mode - self.BLINK_MODE
        else:
            return self._mode

    def set_mode(self, mode):
        """
        Sets pad mode
        :param mode: The desired mode - blink mode may be combined with all others
        """
        self._mode = mode

    def set_switch_state(self, state):
        if self.get_mode() == self.SWITCH_MODE and (state == self.OFF or state == self.ON):
            self._state = state
            return True
        else:
            return False

    def note_on(self, velocity):
        mode = self.get_mode()
        if mode == self.SWITCH_MODE:
            if self._state == self.ON:
                self._state = self.OFF
            else:
                self._state = self.ON
            return self._state
        elif mode == self.PUSH_MODE:
            self._state = self.ON
            return self._state
        elif mode == self.PAD_MODE:
            self._state = self.ON
            return velocity
        else:
            return None

    def note_off(self):
        mode = self.get_mode()
        if mode == self.SWITCH_MODE:
            return self._state
        elif mode == self.PUSH_MODE or mode == self.PAD_MODE:
            self._state = self.OFF
            return self._state
        else:
            return None


class Pads:
    """
    Class that defines a full array of pads (8 pads in each program so 4 X 8 = 32 pads in total
    """

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

    def get_mode(self, program, pad):
        return self._pads[program][self._pad_index[pad]].get_mode()

    def set_mode(self, program, pad, mode):
        self._pads[program][self._pad_index[pad]].set_mode(mode)

    def note_on(self, program, pad, velocity):
        return self._pads[program][self._pad_index[pad]].note_on(velocity)

    def note_off(self, program, pad):
        return self._pads[program][self._pad_index[pad]].note_off()

    def set_switch_state(self, program, pad, state):
        return self._pads[program][self._pad_index[pad]].set_switch_state(state)

    def get_state(self, program, pad):
        return self._pads[program][self._pad_index[pad]].get_state()
