import neurolab as nl
import numpy as np
import pickle
from word_tone import text2color
from random import shuffle

def create_worker():
	net = nl.net.newelm([[0, 1], [0, 1], [0, 1]], [15, 1]) 

	with open("normalized_trainset", "rb") as f:
		trainset = pickle.load(f)

	examples = []
	target = []

	shuffle(trainset)
	for exmpl in trainset[:500]:
		examples.append(exmpl[0])
		target.append([float(exmpl[1])])

	net_input = np.array(examples).reshape(len(examples), len(examples[0]))
	net_target = np.array(target).reshape(len(target), len(target[0]))

	#print("net_input:\n", net_input)
	#print("net_target:\n", net_target)

	error = net.train(net_input, net_target, epochs=1000, show=10, goal=0.1)

	print(min(error))

	with open("nn_worker", "wb") as f:
		pickle.dump(net, f)

	return net

def create_judge(worker):
	net = nl.net.newff([[0, 1]], [10, 1]) 

	with open("normalized_trainset", "rb") as f:
		trainset = pickle.load(f)

	examples = []
	target = []

	for exmpl in trainset:
		exmpl[0] = [exmpl[0]]
		examples.append(worker.sim(np.array(exmpl[0]).reshape(len(exmpl[0]), len(exmpl[0][0]))))
		target.append([float(exmpl[1])])

	net_input = np.array(examples).reshape(len(examples), len(examples[0]))
	net_target = np.array(target).reshape(len(target), len(target[0]))

	error = net.train(net_input, net_target, epochs=2000, show=10, goal=0.05)

	print(min(error))

	with open("nn_judge", "wb") as f:
		pickle.dump(net, f)

def main():
	create_worker()

if __name__ == '__main__':
	main()