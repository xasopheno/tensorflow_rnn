import random
import time
import rtmidi

midiout = rtmidi.MidiOut()
# available_ports = midiout.get_ports()
midiout.open_port(0)

# full = .3

long = .13
short = .1

for i in range(4):
    for i in range(33):
        print (i + 1)
        for i in range(40, 80, i + 3):
            note_on = [0x90, i, 120] # channel 1, middle C, velocity 112
            note_off = [0x80, i, 0]
            midiout.send_message(note_on)
            time.sleep(short)
            midiout.send_message(note_off)

            note_on = [0x90, 120 - i, 120] # channel 1, middle C, velocity 112
            note_off = [0x80, 120 - i, 0]
            midiout.send_message(note_on)
            time.sleep(long)
            midiout.send_message(note_off)

del midiout
