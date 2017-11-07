import tensorflow as tf
import numpy as np
import random
import time
import sys
import subprocess
from NeuralNetwork import Network


ckpt_file = ""
TEST_PREFIX = "55 55 55 55 55 55 55 55" # Prefix to prompt the network in test mode

print ("Usage:")
print ('\t\t ', sys.argv[0], ' [ckpt model to load] [prefix, e.g., "55 55 55 55 55 "]')
if len(sys.argv)>=2:
    ckpt_file=sys.argv[1]
if len(sys.argv)==3:
    TEST_PREFIX = sys.argv[2]


def embed_to_vocab(data_, vocab, predict=False):
    if ckpt_file == "":
        # TRAIN
        data = np.zeros((len(data_), len(vocab)))

        count=0
        for s in data_:
            v = [0.0]*len(vocab)
            v[vocab.index(s)] = 1.0
            data[count, :] = v
            count += 1

        return data

    else:
        # PREDICT
        if predict:
            data_ = data_.replace("'", "")

        data = np.zeros((len(data_), len(vocab)))
        count=0

        if predict:
            s = data_
            v = [0.0]*len(vocab)
            v[vocab.index(s)] = 1.0
            data[count, :] = v
            count += 1
        else:
            for s in data_[:0]:
                s = s.replace(',', '')
                v = [0.0]*len(vocab)
                v[vocab.index(s)] = 1.0
                data[count, :] = v
                count += 1
        return data


## Load the data
data_ = ""
with open('datasets/compressed/first.txt', 'r') as f:
    data_ += f.read()
data_ = data_.split(' ')
# data_ = data_[1::1]

# print ('4_data', data_)
## Convert to 1-hot coding
vocab = sorted(list(set(data_)))
print(vocab)

data = embed_to_vocab(data_, vocab,
                      # predict=True,
                      )
in_size = out_size = len(vocab)
lstm_size = 128 #128s
num_layers = 2
batch_size = 128 #128
time_steps = 50 #50

NUM_TRAIN_BATCHES = 50

LEN_TEST_TEXT = 2000 # Number of test characters of text to generate after training the network
ckpt_filename = 'model'
midi_filename = 'midiOut.txt'



## Initialize the network
config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.InteractiveSession(config=config)

net = Network(in_size = in_size,
                   lstm_size = lstm_size,
                   num_layers = num_layers,
                   out_size = out_size,
                   session = sess,
                   learning_rate = 0.003,
                   name = "char_rnn_network")

sess.run(tf.global_variables_initializer())

saver = tf.train.Saver(tf.global_variables())


## 1) TRAIN THE NETWORK
if ckpt_file == "":
    last_time = time.time()

    batch = np.zeros((batch_size, time_steps, in_size))
    batch_y = np.zeros((batch_size, time_steps, in_size))

    possible_batch_ids = range(data.shape[0]-time_steps-1)

    for i in range(NUM_TRAIN_BATCHES):
        # Sample time_steps consecutive samples from the dataset text file
        batch_id = random.sample( possible_batch_ids, batch_size )

        for j in range(time_steps):
            ind1 = [k+j for k in batch_id]
            ind2 = [k+j+1 for k in batch_id]

            batch[:, j, :] = data[ind1, :]
            batch_y[:, j, :] = data[ind2, :]

        cst = net.train_batch(batch, batch_y)
        # print(cst)

        # if (i % 1) == 0:
        #     print('batch: ', i)

        if (i % 1) == 0:
            new_time = time.time()
            diff = new_time - last_time
            last_time = new_time

            print ("batch: ",i,"   loss: ",cst,"   speed: ",(100.0/diff)," batches / s")

            saver.save(sess, "saved/" + ckpt_filename + ".ckpt")
            subprocess.call("python rnn_tf.py saved/" + ckpt_filename + ".ckpt [60,20]", shell=True)
            subprocess.call("python Midi/compressed_midi_player.py", shell=True)

    saver.save(sess, "saved/" + ckpt_filename + ".ckpt")


# 2) GENERATE LEN_TEST_TEXT CHARACTERS USING THE TRAINED NETWORK
if ckpt_file != "":
    saver.restore(sess, ckpt_file)
    print("using ckpt_file: ", ckpt_file)

TEST_PREFIX = TEST_PREFIX.split(' ')
print ('TEST_PREFIX', TEST_PREFIX)
for i in range(len(TEST_PREFIX)):
    out = net.run_step( embed_to_vocab(TEST_PREFIX[i], vocab, predict=True), i==0)

gen_str = TEST_PREFIX
# print ('!!!_gen_str): ', gen_str)
for i in range(LEN_TEST_TEXT):
    element = np.random.choice( range(len(vocab)), p=out ) # Sample character from the network according to the generated output probabilities
    gen_str += [vocab[element]]
    out = net.run_step(embed_to_vocab(vocab[element], vocab, predict=True), False)
# print ('final_string', gen_str)

with open(midi_filename, "w") as f:
    f.seek(0)
    f.truncate()
    f.write(str(gen_str))



