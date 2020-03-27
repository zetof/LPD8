from lpd8.lpd8 import LPD8
from lpd8.programs import Programs
from lpd8.pads import Pad, Pads
from lpd8.knobs import Knobs
from lpd8.pgm_chg import Pgm_Chg
from test import Test
from time import sleep

# This object is created to test different callbacks from LPD8 class
test = Test()

# Create an LPD8 object and try to start it (open MIDI in and out communication)
lpd8 = LPD8()
lpd8.start()

# In all following settings, we will define limits / actions for PROGRAM 4
# Define control knob 1 limits from -1 to 1 and set increments to float values
# Define control knob 2 limits from 0 to 100 with 10 steps (limit values to 0, 10, 20, ..., 90, 100)
# Knobs that have no definition range from 0..127 with integer increments of 1 (default MIDI behaviour)
lpd8.set_knob_limits(Programs.PGM_4, Knobs.KNOB_1, -1, 1, is_int=False)
lpd8.set_knob_limits(Programs.PGM_4, Knobs.KNOB_2, 0, 100, steps=10)

# Sets An initial value for knob 3 to 63
lpd8.set_knob_value(Programs.PGM_4, Knobs.KNOB_3, 63)

# Set different modes for pads
# Note that we can define modes for a single pad, an array of pads or all pads
# Pads 1 and two will blink and will be in switch mode (every push changes state between 0 and 1)
# Pad 3 won't blink but will be in switch mode too
# Pad 4 will be in push mode, sending a 1 at every NOTE ON event and a 0 at every NOTE OFF event
# Pads that have no definition are set in classical pad mode with NOTE ON / NOTE OFF events and velocity values
lpd8.set_pad_mode(Programs.PGM_4, [Pads.PAD_1, Pads.PAD_2], Pad.SWITCH_MODE + Pad.BLINK_MODE)
lpd8.set_pad_mode(Programs.PGM_4, Pads.PAD_3, Pad.SWITCH_MODE)
lpd8.set_pad_mode(Programs.PGM_4, Pads.PAD_4, Pad.PUSH_MODE)

# Subscribe to different events and map them to a method in test object
# Note that we can subscribe events for a single object, an array of objects or all objects of a group
lpd8.subscribe(test, test.ctrl_value, Programs.PGM_4, LPD8.CTRL, Knobs.ALL_KNOBS)
lpd8.subscribe(test, test.note_on_value, Programs.PGM_4, LPD8.NOTE_ON, Pads.ALL_PADS)
lpd8.subscribe(test, test.note_off_value, Programs.PGM_4, LPD8.NOTE_OFF, Pads.ALL_PADS)
lpd8.subscribe(test, test.pgm_change, Programs.PGM_4, LPD8.PGM_CHG, Pgm_Chg.PGM_CHG_4)

# We loop as long as test class allows it
while test.is_running():

    # Every loop, we update pads status (blink, ON or OFF)
    # This method returns True if LPD8 pad is still running, False otherwise
    if lpd8.pad_update():
        sleep(.5)
    else:

        # If LPD8 pad is not running anymore, we leave the loop
        test.stop()

# We tidy uo things and kill LPD8 process
lpd8.stop()