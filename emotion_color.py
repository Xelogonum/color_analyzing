import neurolab as nl
import numpy as np

gray   = [128, 128, 128]
blue   = [0, 0, 255]
green  = [0, 128, 0]
red    = [255, 0, 0]
yellow = [255, 255, 0]
violet = [238, 130, 238]
brown  = [100, 40, 0] 
black  = [0, 0, 0]

emotions = ("interest", "happieness", "surpirse", "sadness", "anger", "disgust", "shame", "fear", "fatigue")

emotion_color = {
				tuple(gray): {"interest": 0.06, "happieness": 0.04, "surpirse": 0.02, "sadness": 0.27, "anger": 0.01, "disgust": 0.15, "shame": 0.18, "fear": 0.12, "fatigue": 0.53},
				tuple(blue): {"interest": 0.27, "happieness": 0.04, "surpirse": 0.02, "sadness": 0.27, "anger": 0.05, "disgust": 0.07, "shame": 0.13, "fear": 0.15, "fatigue": 0.08},
				tuple(green): {"interest": 0.26, "happieness": 0.10, "surpirse": 0.26, "sadness": 0.13, "anger": 0.08, "disgust": 0.07, "shame": 0.19, "fear": 0.08, "fatigue": 0.07},
				tuple(red): {"interest": 0.16, "happieness": 0.52, "surpirse": 0.23, "sadness": 0.4, "anger": 0.55, "disgust": 0.04, "shame": 0.04, "fear": 0.17, "fatigue": 0.02},
				tuple(yellow): {"interest": 0.20, "happieness": 0.24, "surpirse": 0.56, "sadness": 0.01, "anger": 0.09, "disgust": 0.19, "shame": 0.12, "fear": 0.15, "fatigue": 0.01},
				tuple(violet): {"interest": 0.05, "happieness": 0.12, "surpirse": 0.14, "sadness": 0.12, "anger": 0.06, "disgust": 0.22, "shame": 0.16, "fear": 0.07, "fatigue": 0.12}, 
				tuple(brown): {"interest": 0.10, "happieness": 0.08, "surpirse": 0.03, "sadness": 0.14, "anger": 0.04, "disgust": 0.27, "shame": 0.17, "fear": 0.03, "fatigue": 0.23}, 
				tuple(black): {"interest": 0.10, "happieness": 0.02, "surpirse": 0.02, "sadness": 0.22, "anger": 0.38, "disgust": 0.18, "shame": 0.13, "fear": 0.43, "fatigue": 0.24}
				}

def dict_to_array(color):
	return [emotion_color[color][emotion] for emotion in emotions]	

def classify_color(net, color):
	result = net.sim(np.array(color).reshape(len(color), len(color[0])))

	print(color[0])
	for value, emotion in zip(result[0], emotions):
		print(emotion + ": " + str(value))

def main():
	net = nl.net.newff([[0, 1], [0, 1], [0, 1]], [5, 5, 5, 9])

	train_set = []
	target = []

	for color in emotion_color:
		target.append(dict_to_array(color))
		train_set.append(color)


	net_input = np.array(train_set).reshape(len(train_set), len(train_set[0]))
	net_target = np.array(target).reshape(len(target), len(target[0]))

	print("net_input:", net_input)
	print("net_target:", net_target)

	error = net.train(net_input, net_target, epochs=2000, show=10, goal=0.2)

	for test_color in [[[256, 256, 256]], [[204, 0, 0]], [[51, 204, 51]]]:
		classify_color(net, test_color)

if __name__ == '__main__':
	main()