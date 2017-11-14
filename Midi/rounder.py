import math
import ast

def round_down(x):
    return int(math.floor(x / 1000.0)) * 1000

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
            length = round_down(length)
            token = ''
            # if midi_num == 0 and length > 3000:
                # token = '|'

            rounded_data.write('[' + str(midi_num) + ',' + str(length) + ']' + token + ' ')


"""



"""
