from __future__ import division
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
current_path = os.getcwd()
import time
import rtmidi
import random

midiout = rtmidi.MidiOut()
# available_ports = midiout.get_ports()
midiout.open_port(0)



class MidiPlayer:
    def __init__(self):
        self.subdivision = 0.07
        self.last_value = 0

    def play_midi(self, value):
        print (value)
        # self.send_midi(value, self.subdivision)
        # self.sendMidi(value + 4, .001)
        # self.sendMidi(value, .01)
        # self.sendMidi(value, .01)
        # self.sendMidi(value + 11, .001)
        # self.sendMidi(value - 10, 0.001)
        # self.sendMidi(value, .001)
        # self.sendMidi(value + 6, .001)
        # self.sendMidi(value, .001)

    def play_silence(self):
        # print(0)
        time.sleep(self.subdivision)

    def start_midi(self, num):
        note_on = [0x90, num, 120] # channel 1, middle C, velocity 112
        time.sleep(self.subdivision)
        midiout.send_message(note_on)

    def stop_midi(self, num):
        note_off = [0x80, num, 120]
        midiout.send_message(note_off)

with open('midiOut.txt', 'r') as f:
    midi_player = MidiPlayer()
    values = f.read().split()
    for value in values:
        value = value.replace("'", "")
        value = value.replace(",", "")
        value = value.replace("[", "")
        value = value.replace("]", "")
        value = int(value)

        # print(value != midi_player.last_value)

        if value != midi_player.last_value:
            try:
                midi_player.stop_midi(midi_player.last_value)
            except:
                print('value was unstoppable', value)

        try:
            if int(value) is not 0 and value != midi_player.last_value:
                rand = random.randint(20, 30)
                midi_player.start_midi(int(value))
                midi_player.start_midi(int(value)+random.randint(20, 30))
                midi_player.start_midi(int(value)+random.randint(20, 30))
                midi_player.start_midi(int(value)+random.randint(20, 30))
                # print(value)
            else:
                midi_player.play_silence()
                # print(value)
        except:
            print('value was unplayable', value)
            midi_player.play_silence()

        midi_player.last_value = value
