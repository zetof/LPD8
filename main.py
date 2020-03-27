from lpd8.lpd8 import LPD8
from lpd8.programs import Programs
from lpd8.pads import Pad, Pads
from lpd8.knobs import Knobs
from lpd8.pgm_chg import Pgm_Chg
from test import Test
from time import sleep

test = Test()

lpd8 = LPD8()
lpd8.start()

lpd8.set_knob_limits(Programs.PGM_4, Knobs.KNOB_1, -1, 1, is_int=False)
lpd8.set_knob_value(Programs.PGM_4, Knobs.KNOB_2, 63)
lpd8.set_pad_mode(Programs.PGM_4, [Pads.PAD_1, Pads.PAD_2], Pad.SWITCH_MODE + Pad.BLINK_MODE)
lpd8.set_pad_mode(Programs.PGM_4, Pads.PAD_3, Pad.SWITCH_MODE)
lpd8.set_pad_mode(Programs.PGM_4, Pads.PAD_4, Pad.PUSH_MODE)
lpd8.subscribe(test, test.ctrl_value, Programs.PGM_4, LPD8.CTRL, Knobs.ALL_KNOBS)
lpd8.subscribe(test, test.note_on_value, Programs.PGM_4, LPD8.NOTE_ON, Pads.ALL_PADS)
lpd8.subscribe(test, test.note_off_value, Programs.PGM_4, LPD8.NOTE_OFF, Pads.ALL_PADS)
lpd8.subscribe(test, test.pgm_change, Programs.PGM_4, LPD8.PGM_CHG, Pgm_Chg.PGM_CHG_4)

while test.is_running():
    if lpd8.pad_update():
        sleep(.5)
    else:
        test.stop()
lpd8.stop()