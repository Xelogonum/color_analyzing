import nltk
from nltk.corpus import movie_reviews
from random import shuffle
from word_tone import text2color
import pickle

with open("words2color_hash", "rb") as f:
	mapped = pickle.load(f)

def find_features(words_list):
	color = text2color(mapped, words_list)
	return {"r": color[0], "g": color[1], "b": color[2]}

documents = []

def setup_words():
	with open("pos", "r") as f:
		pos = f.read().split(",")
	with open("neg", "r") as f:
		neg = f.read().split(",")

	with open("trainset", "w") as f:
		for category in (pos, neg):
			for word in category:
				if category == pos:
					feature = (find_features(list(word.lower())), "pos")
					documents.append(feature)
					f.write(str(feature) + ",")
				else:
					feature = (find_features(list(word.lower())), "neg")
					documents.append(feature)
					f.write(str(feature) + ",")
			print("Ended one part")

def setup_reviews():
	global documents
	documents += [(find_features(list(movie_reviews.words(fileid))), category) for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]

class SentimentClassifier(nltk.classify.ClassifierI):
	def __init__(self):
		self.judges = []
		setup_reviews()

	def train_judges(self, docs):
		for i in range(10):
			print("Training classifier # %s" % (i+1))

			shuffle(docs)

			train_set, test_set = docs[100:], docs[:100]

			classifier = nltk.classify.NaiveBayesClassifier.train(train_set)

			find_accuracy(classifier, test_set)

			self.judges.append(classifier)

	def train_cheif(self, docs):
		self.train_judges(docs)

		shuffle(docs)

		cheif_docs = []
		for doc in docs:
			cheif_docs.append(({i: self.judges[i].classify(doc[0]) for i in range(10)}, doc[1]))

		self.cheif = nltk.classify.NaiveBayesClassifier.train(cheif_docs[100:])

		find_accuracy(self.cheif, cheif_docs[:100])

	def classify(self, featureset):

		cheif_featureset = {i: self.judges[i].classify(featureset) for i in range(10)}

		return self.cheif.classify(cheif_featureset)

def find_accuracy(classifier, docs):
	number = 0
	correct = 0
	incorrect = 0
	for example in docs:
		if classifier.classify(example[0]) == example[1]:
			correct += 1
		else:
			incorrect += 1
		number += 1
	print("Number of examples: {}\nCorrect: {}\nIncorrect: {}\nAccuracy: {}\n".format(number, correct, incorrect, correct / number))

if __name__ == "__main__":
	'''
	classifier = SentimentClassifier()
	classifier.train(documents[50:])

	with open("MultiNaiveBayesClassifier", "wb") as file:
		pickle.dump(classifier, file)

	with open("words2color_hash", "wb") as file:
		pickle.dump(mapped, file)

	print(nltk.classify.accuracy(classifier, documents[:50]))
	'''
	classifier = SentimentClassifier()
	classifier.train_cheif(documents[50:])

	with open("SentimentClassifier", "wb") as file:
		pickle.dump(classifier, file)

	find_accuracy(classifier, documents[:50])