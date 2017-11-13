from __future__ import division
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
current_path = os.getcwd()
from NoteToMidi import sendMidi
import time
import ast
import random
import rtmidi

midiout = rtmidi.MidiOut()
# available_ports = midiout.get_ports()
midiout.open_port(0)


subdivision = 0.01
last_value = 0
counter = 0

def play_midi(value, length = 1):
    # print (value)
    # sendMidi(value, length + subdivision)
    note_on = [0x90, value, 120] # channel 1, middle C, velocity 112
    midiout.send_message(note_on)
    time.sleep(subdivision * length)
    note_off = [0x80, value, 120]
    midiout.send_message(note_off)

    # sendMidi(value + 20, .001)
    # sendMidi(value, .01)
    # sendMidi(value, .01)
    # sendMidi(value + 11, .001)
    # sendMidi(value - 10, 0.001)
    # sendMidi(value, .001)
    # sendMidi(value + 6, .001)
    # sendMidi(value, .001)

# def sendMidi(num, length):
#     note_on = [0x90, value, 120] # channel 1, middle C, velocity 112
    # note_off = [0x80, num, 120]
    # midiout.send_message(note_on)
    # time.sleep(length)zx
    # midiout.send_message(note_off)

def play_silence(length):
    # print(0)
    time.sleep(length * subdivision)

with open('midiOut.txt', 'r') as f:
    values = f.read().split(' ')
    for value in values:
        value = value.replace("', '", " ")
        value = value.replace("[,", "")
        value = value.replace("['", "")
        value = value.replace(",]", "")
        value = value.replace("',", "")
        value = value.replace("'", "")
        value = value.replace("]]", "]")
        value = ast.literal_eval(value)
        # print(value)
        midi_num = int(value[0])
        length = int(value[1]) / 350
        try:
            if midi_num is not 0:
                print(midi_num, length)
                play_midi(midi_num, length)
                # print(value)
            else:
                play_silence(length)
                # print(value)
        except:
            print('value was unplayable', value)
            play_silence(length)

        counter += 1
