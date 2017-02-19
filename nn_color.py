import neurolab as nl
import numpy as np
import pickle
from word_tone import text2color

net = nl.net.newff([[0, 1], [0, 1], [0, 1]], [17, 1], [nl.trans.PureLin()]*2) 

with open("normalized_trainset", "rb") as f:
	trainset = pickle.load(f)

examples = []
target = []

for exmpl in trainset:
	examples.append(exmpl[0])
	target.append([float(exmpl[1])])

net_input = np.array(examples).reshape(len(examples), len(examples[0]))
net_target = np.array(target).reshape(len(target), len(target[0]))

error = net.train(net_input, net_target, epochs=2000, show=10, goal=0.1)

print(min(error))

with open("color_nn", "wb") as f:
	pickle.dump(net, f)

with open("words2color_hash", "rb") as f:
	mapped = pickle.load(f)

def give_label(word):
	color = text2color(mapped, word)
	normalized_color = [[color[0]/255, color[1]/255, color[2]/255]]

	out = net.sim(np.array(normalized_color).reshape(len(normalized_color), len(normalized_color[0])))
	print(out)

def main():
	while True:
		give_label(input("Enter: ").lower())

main()