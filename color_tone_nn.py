import pickle
import neurolab as nl
import numpy as np
from word_tone import text2color

with open("nn_worker", "rb") as f:
	net_worker = pickle.load(f)

with open("nn_judge", "rb") as f:
	net_judge = pickle.load(f)

with open("words2color_hash", "rb") as f:
	mapped = pickle.load(f)

with open("normalized_trainset", "rb") as f:
	trainset = pickle.load(f)

def find_accuracy():
	number = 0
	correct = 0
	incorrect = 0
	for example in trainset:
		print(example)
		example[0] = [example[0]]
		if net.sim(np.array(example[0]).reshape(len(example[0]), len(example[0][0]))) < 0.55:
			result = 0
		else:
			result = 1

		if result == example[1]:
			correct += 1
		else:
			incorrect += 1
		number += 1
	print("Number of examples: {}\nCorrect: {}\nIncorrect: {}\nAccuracy: {}\n".format(number, correct, incorrect, correct / number))

def give_label(word):
	color = text2color(mapped, word)
	normalized_color = [[color[0]/255, color[1]/255, color[2]/255]]

	worker_out = net_worker.sim(np.array(normalized_color).reshape(len(normalized_color), len(normalized_color[0])))
	print(worker_out)

	#judge_out = net_judge.sim(np.array(worker_out).reshape(len(worker_out), len(worker_out[0])))
	#print(judge_out)

def main():
	while True:
		give_label(input("Enter: ").lower())

main()