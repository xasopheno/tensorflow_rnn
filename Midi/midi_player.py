from __future__ import division
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
current_path = os.getcwd()
from NoteToMidi import sendMidi
import time

subdivision = 0.04
last_value = 0
counter = 0

def play_midi(value):
    # print (value)
    sendMidi(value, subdivision)
    # sendMidi(value + 20, .001)
    # sendMidi(value, .01)
    # sendMidi(value, .01)
    # sendMidi(value + 11, .001)
    # sendMidi(value - 10, 0.001)
    # sendMidi(value, .001)
    # sendMidi(value + 6, .001)
    # sendMidi(value, .001)

def play_silence():
    # print(0)
    time.sleep(subdivision * .95)

with open('midiOut.txt', 'r') as f:
    values = f.read().split()
    for value in values:
        if counter % 2 == True:
        # if counter % 1 == True:
            value = value.replace("'", "")
            value = value.replace(",", "")
            # print(value)

            try:
                if int(value) is not 0:
                    play_midi(int(value))
                    # print(value)
                else:
                    play_silence()
                    # print(value)
            except:
                print('value was unplayable', value)
                play_silence()

        counter += 1
