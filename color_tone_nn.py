import pickle
import neurolab as nl
import numpy as np
from word_tone import text2color

with open("color_nn", "rb") as f:
	net = pickle.load(f)

with open("words2color_hash", "rb") as f:
	mapped = pickle.load(f)

def give_label(word):
	color = text2color(mapped, word)
	normalized_color = [[color[0]/255, color[1]/255, color[2]/255]]

	out = net.sim(np.array(normalized_color).reshape(len(normalized_color), len(normalized_color[0])))

	print(out)
	if out[0][0] > 0.54:
		print("Negative")
	else:
		print("Positive")

def main():
	while True:
		give_label(input("Enter: ").lower())

main()