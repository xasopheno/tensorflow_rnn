import math
import ast

def rounddown(x):
    return int(math.floor(x / 10.0)) * 10

with open('midiOut.txt', 'r') as f:
    with open("rounded.txt", 'a') as rounded_data:
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
            length = int(value[1])
            length = rounddown(length)

            rounded_data.write('[' + str(midi_num) + ',' + str(length) + '] ')
