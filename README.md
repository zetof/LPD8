# lpd8
### A Python library to interface an AKAI LPD8 pad device
![AKAI LPD8](https://d1jtxvnvoxswj8.cloudfront.net/catalog/product/cache/421fe9f256d7dd674b5a25e9478e383f/l/p/lpd8_web_large.jpg_2a5e9928f9c871bf86f5a4d05b4453e6.jpg)

This little library is designed to help the integration of an AKAI LPD8 pad into a Python program.
It is easy to integrate and simple to use. Based on the rtmidi library, it uses MIDI messages to
communicate with the LPD8 device and reads messages coming from it.
In PAD mode, it allows some pads to blink or to have an ON (light on) and OFF (light off) state.
It allows the use of 4 programs and has a sticky mode for knob controls, meaning that the library
stores knob states for each program and only reacts to a knob if its value is set to its previous state
for a given program.
Knob limits and behaviours are configurable, so are pads.
It uses a subscription mechanism for each event, allowing triggering of specific methods of objects. These methods
may then implement other MIDI or OSC events or pilot a visual interface.

### Example of use
```python
from lpd8.lpd8 import LPD8
from lpd8.programs import Programs
from lpd8.pads import Pad, Pads
from lpd8.knobs import Knobs
from lpd8.pgm_chg import Pgm_Chg
from consummer import Consummer
from time import sleep

# This object is created to test different callbacks from LPD8 class
consummer = Consummer()

# Create an LPD8 object and try to start it (open MIDI in and out communication)
lpd8 = LPD8()
lpd8.start()

# In normal times, a control knob is meant to be sticky. That means that if we change program and then knob
# value, knob will not react when we return to original program until last stored value for this program
# will be reached. It will then follow changes normally
# Note that we can define sticky mode for a single knob, an array of knobs or all knobs
lpd8.set_not_sticky_knob(Programs.PGM_4, [Knobs.KNOB_1, Knobs.KNOB_2, Knobs.KNOB_3, Knobs.KNOB_4])

# In all following settings, we will define limits / actions for PROGRAM 4
# Define control knob 1 limits from -1 to 1 and set increments to float values
# Define control knob 2 limits from 0 to 100 with 10 steps (limit values to 0, 10, 20, ..., 90, 100)
# Knobs that have no definition range from 0..127 with integer increments of 1 (default MIDI behaviour)
lpd8.set_knob_limits(Programs.PGM_4, Knobs.KNOB_1, -1, 1, is_int=False)
lpd8.set_knob_limits(Programs.PGM_4, Knobs.KNOB_2, 0, 100, steps=10)

# Set An initial value for knob 3 to 63
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

# For a pad of type SWITCH, sets the initial state of pad
# Note that we can define modes for a single pad, an array of pads or all pads
lpd8.set_pad_switch_state(Programs.PGM_4, [Pads.PAD_1, Pads.PAD_3], Pad.ON)

# Subscribe to different events and map them to a method in test object
# Note that we can subscribe events for a single object, an array of objects or all objects of a group
lpd8.subscribe(consummer, consummer.ctrl_value, Programs.PGM_4, LPD8.CTRL, Knobs.ALL_KNOBS)
lpd8.subscribe(consummer, consummer.note_on_value, Programs.PGM_4, LPD8.NOTE_ON, Pads.ALL_PADS)
lpd8.subscribe(consummer, consummer.note_off_value, Programs.PGM_4, LPD8.NOTE_OFF, Pads.ALL_PADS)
lpd8.subscribe(consummer, consummer.pgm_change, Programs.PGM_4, LPD8.PGM_CHG, Pgm_Chg.PGM_CHG_4)

# We loop as long as test class allows it
while consummer.is_running():

    # Every loop, we update pads status (blink, ON or OFF)
    # This method returns True if LPD8 pad is still running, False otherwise
    if lpd8.pad_update():
        sleep(.5)
    else:

        # If LPD8 pad is not running anymore, we leave the loop
        consummer.stop()

# We tidy up things and kill LPD8 process
lpd8.stop()
```