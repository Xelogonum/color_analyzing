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
		pos = [word.lower() for word in f.read().split(",")]
	with open("neg", "r") as f:
		neg = [word.lower() for word in f.read().split(",")]

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
		setup_words()

	def train(self, docs):
		for i in range(10):
			print("Training classifier # %s" % (i+1))

			shuffle(docs)

			train_set, test_set = docs[100:], docs[:100]

			classifier = nltk.classify.NaiveBayesClassifier.train(train_set)

			print("\tAccuracy:", nltk.classify.accuracy(classifier, test_set))
			print()

			self.judges.append(classifier)

	def classify(self, featureset):
		pos = 0
		neg = 0

		for judge in self.judges:
			if judge.classify(featureset) == "pos":
				pos += 1
			elif judge.classify(featureset) == "neg":
				neg += 1

		if pos < neg:
			return "neg"
		elif pos >= neg:
			return "pos"

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
	classifier.train(documents[50:])

	with open("SentimentClassifier", "wb") as file:
		pickle.dump(classifier, file)

	print(nltk.classify.accuracy(classifier, documents[:50]))