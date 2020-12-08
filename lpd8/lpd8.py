import rtmidi
from threading import Thread, Timer
from time import sleep
from lpd8.dispatcher import Dispatcher
from lpd8.programs import Programs
from lpd8.knobs import Knobs
from lpd8.pads import Pad, Pads

class LPD8(Thread):
    """
    Main class defining the LPD8 object
    """

    NAME = 'LPD8'
    DELAY = 1
    NOTE_ON = 144
    NOTE_OFF = 128
    CTRL = 176
    PGM_CHG = 192
    BLINK = 100

    def __init__(self, program=4):
        self._program = program
        self._delay = self.DELAY / 1000
        self._blink = self.BLINK / 1000
        self._dispatcher = Dispatcher()
        self._pads = Pads()
        self._knobs = Knobs()
        self.connect()

    def _get_midi_device(self, devices_list):
        midi_device = None
        midi_ports = devices_list.get_ports()
        if len(midi_ports) != 0:
            index = 0
            for name in midi_ports:
                if name.find(self.NAME) != -1:
                    devices_list.open_port(index)
                    midi_device = devices_list
                index += 1
        return midi_device

    def _read_midi(self):
        msg = self._midi_in.get_message()
        if msg is not None:
            cmd = msg[0][0]
            ctrl = msg[0][1]

            if cmd <= self.NOTE_OFF + Programs.PGM_MAX:
                pad_value = self._pads.note_off(cmd - self.NOTE_OFF + 1, ctrl)
                if pad_value is not None:
                    if pad_value == Pad.ON:
                        self.pad_on(cmd - self.NOTE_OFF + 1, [ctrl])
                    self._dispatcher.notify(cmd - self.NOTE_OFF + 1, self.NOTE_OFF, ctrl, pad_value)

            elif cmd <= self.NOTE_ON + Programs.PGM_MAX:
                pad_value = self._pads.note_on(cmd - self.NOTE_ON + 1, ctrl, msg[0][2])
                if pad_value is not None:
                    self._dispatcher.notify(cmd - self.NOTE_ON + 1, self.NOTE_ON, ctrl, pad_value)

            elif cmd <= self.CTRL + Programs.PGM_MAX:
                if ctrl <= Knobs.KNOB_MAX:
                    knob_value = self._knobs.get_value(cmd - self.CTRL + 1, ctrl, msg[0][2])
                    if knob_value is not None:
                        self._dispatcher.notify(cmd - self.CTRL + 1, self.CTRL, ctrl, knob_value)

            elif cmd <= self.PGM_CHG + Programs.PGM_MAX:
                self._dispatcher.notify(cmd - self.PGM_CHG + 1, self.PGM_CHG, ctrl + 1)

    def run(self):
        while self._running:
            self._read_midi()
            sleep(self._delay)

    def stop(self):
        self._running = False

    def is_running(self):
        return self._running

    def connect(self):
        self._midi_in = self._get_midi_device(rtmidi.MidiIn())
        self._midi_out = self._get_midi_device(rtmidi.MidiOut())
        if self._midi_in is not None and self._midi_out is not None:
            self._running = True
        else:
            self._running = False
            print("*** No LPD8 Controller found ***")
        Thread.__init__(self)

    def subscribe(self, callback_class, callback_method, program, event_type, object_ids):
        if isinstance(object_ids, list):
            for object_id in object_ids:
                self._dispatcher.subscribe(callback_class, callback_method, program, event_type, object_id)
        else:
            self._dispatcher.subscribe(callback_class, callback_method, program, event_type, object_ids)

    def unsubscribe(self, program, event_type, object_id=None):
        self._dispatcher.unsubscribe(program, event_type, object_id)

    def set_knob_limits(self, program, knobs, min_value, max_value, is_int=True, steps=0):
        if isinstance(knobs, list):
            for knob in knobs:
                self._knobs.set_limits(program, knob, min_value, max_value, is_int, steps)
        else:
            self._knobs.set_limits(program, knobs, min_value, max_value, is_int, steps)

    def set_knob_value(self, program, knobs, value):
        if isinstance(knobs, list):
            for knob in knobs:
                self._knobs.set_value(program, knob, value)
        else:
            self._knobs.set_value(program, knobs, value)

    def set_pad_mode(self, program, pads, mode):
        if isinstance(pads, list):
            for pad in pads:
                self._pads.set_mode(program, pad, mode)
        else:
            self._pads.set_mode(program, pads, mode)

    def set_sticky_knob(self, program, knobs):
        if isinstance(knobs, list):
            for knob in knobs:
                self._knobs.set_sticky(program, knob)
        else:
            self._knobs.set_sticky(program, knobs)

    def set_not_sticky_knob(self, program, knobs):
        if isinstance(knobs, list):
            for knob in knobs:
                self._knobs.set_not_sticky(program, knob)
        else:
            self._knobs.set_not_sticky(program, knobs)

    def set_pad_switch_state(self, program, pads, state):
        if isinstance(pads, list):
            for pad in pads:
                self._pads.set_switch_state(program, pad, state)
        else:
            self._pads.set_switch_state(program, pads, state)

    def pad_update(self):
        if  self._running:
            on_array = []
            off_array = []
            blink_array = []
            for pad in Pads.ALL_PADS:
                state = self._pads.get_state(self._program, pad)
                if state == Pad.BLINK:
                    blink_array.append(pad)
                elif state != Pad.OFF:
                    on_array.append(pad)
                else:
                    off_array.append(pad)
            self.pad_on(self._program, on_array + blink_array)
            self.pad_off(self._program, off_array)
            blink_timer = Timer(self._blink, self.pad_off, [self._program, blink_array])
            blink_timer.start()
            return True
        else:
            return False

    def pad_on(self, program, pads):
        if self._running:
            for pad in pads:
                note_on = [self.NOTE_ON + program - 1, pad, 1]
                self._midi_out.send_message(note_on)
            return True
        else:
            return False

    def pad_off(self, program, pads):
        if self._running:
            for pad in pads:
                note_off = [self.NOTE_ON + program - 1, pad, 0]
                self._midi_out.send_message(note_off)
            return True
        else:
            return False
