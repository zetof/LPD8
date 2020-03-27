from math import floor
from lpd8.programs import Programs

class Knob:
    """
    Class that defines a single control knob
    """

    _MIDI_STEPS = 127   # Real number of MIDI steps
    _TOLERANCE = 2      # Used to compute sticky effect when changing program

    def __init__(self):
        self._value = None
        self._midi_value = None
        self._sticky = True
        self._sync = 0
        self.set_limits()

    # Adjusts value if it is an integer value or if steps are defined
    def _adjust_value(self, value):
        if self._inc != 0:
            value = floor(value / self._inc) * self._inc
        if self._is_int:
            value = int(value)
        else:
            value = round(value, 2)
        return value

    def get_value(self, midi_value):
        """
        Gets knob real value according to its properties
        :param midi_value: The knob read midi value
        :return: The computed real value according to knob properties
        """
        if self._sticky and not self._midi_value == None:
            gap = self._midi_value - midi_value
            if abs(gap) > self._TOLERANCE and self._sync == 0:
                self._sync = gap
            if self._sync < 0 and midi_value <= self._midi_value or self._sync > 0 and midi_value >= self._midi_value:
                self._sync = 0
        if self._sync == 0:
            self._midi_value = midi_value
            value = self._min_value + (self._max_value - self._min_value) * midi_value / self._MIDI_STEPS
            value = self._adjust_value(value)
            if value == self._value:
                return None
            else:
                self._value = value
                return value

    def set_value(self, value):
        """
        Sets a knob real value, evaluates its associated midi value and stores it
        :param value: The knob real value
        :return: True if value is between minimum and maximum range, false otherwise
        """
        if value >= self._min_value and value <= self._max_value:
            self._midi_value = int(self._MIDI_STEPS * (value - self._min_value) / (self._max_value - self._min_value))
            self._value = self._adjust_value(value)
            return True
        else:
            return False

    def set_sticky(self):
        """
        Sets sticky knob (memory between different programs)
        """
        self._sticky = True

    def set_not_sticky(self):
        """
        Sets not sticky knob (no memory between different programs)
        """
        self._sticky = False

    def set_limits(self, min_value=0, max_value=_MIDI_STEPS, is_int=True, steps=0):
        """
        Sets knob limits and behaviour
        :param min_value: The minimum value (when MIDI value is equal to 0)
        :param max_value: The maximum value (when MIDI value is equal to 127)
        :param is_int: If true, knob will only return integer values (default), otherwise float values
        :param steps: Number of steps between min and max values (O to 100 with 10 steps gives 0, 10, ... increments)
        """
        self._min_value = min_value
        self._max_value = max_value
        self._is_int = is_int
        self._inc = 0
        if steps != 0:
            self._inc = (max_value - min_value) / steps

class Knobs:
    """
    Class that defines a full array of knobs (8 knobs in each program so 4 X 8 = 32 knobs in total
    """

    KNOB_1 = 1
    KNOB_2 = 2
    KNOB_3 = 3
    KNOB_4 = 4
    KNOB_5 = 5
    KNOB_6 = 6
    KNOB_7 = 7
    KNOB_8 = 8

    ALL_KNOBS = [KNOB_1, KNOB_2, KNOB_3, KNOB_4, KNOB_5, KNOB_6, KNOB_7, KNOB_8]
    KNOB_MAX = len(ALL_KNOBS)

    def __init__(self, programs=Programs.PGM_MAX, knobs=KNOB_MAX):
        self._knobs = []
        for program in range(programs + 1):
            self._knobs.append([])
            for knob in range(knobs + 1):
                self._knobs[program].append(Knob())

    def get_value(self, program, knob, midi_value):
        """
        Get the value of a knob from a knob array
        :param program:
        :param knob:
        :param midi_value:
        :return:
        """
        return self._knobs[program][knob].get_value(midi_value)

    def set_limits(self, program, knob, min_value, max_value, is_int=True, steps=0):
        """
        Set knob limits and behaviour in a knob array
        :param program:
        :param knob:
        :param min_value: The minimum value (when MIDI value is equal to 0)
        :param max_value: The maximum value (when MIDI value is equal to 127)
        :param is_int: If true, knob will only return integer values (default), otherwise float values
        :param steps: Number of steps between min and max values (O to 100 with 10 steps gives 0, 10, ... increments)
        :return:
        """
        self._knobs[program][knob].set_limits(min_value, max_value, is_int, steps)

    def set_value(self, program, knob, value):
        """
        Set knob value in a knob array
        :param program:
        :param knob:
        :param value:
        :return:
        """
        self._knobs[program][knob].set_value(value)

    def set_sticky(self, program, knob):
        """
        Set sticky knob in a knob array
        :param program:
        :param knob:
        :return:
        """
        self._knobs[program][knob].set_sticky()

    def set_not_sticky(self, program, knob):
        """
        Set not sticky knob in a knob array
        :param program:
        :param knob:
        :return:
        """
        self._knobs[program][knob].set_not_sticky()
