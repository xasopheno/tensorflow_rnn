import random
import time
import rtmidi

midiout = rtmidi.MidiOut()
# available_ports = midiout.get_ports()
midiout.open_port(0)

# full = .3

long = .13
short = .1

def sendMidi(num, length):
    note_on = [0x90, num, 120] # channel 1, middle C, velocity 112
    note_off = [0x80, num, 120]
    midiout.send_message(note_on)
    time.sleep(length)
    midiout.send_message(note_off)

# del midiout
