import nltk, pickle
from extractor import extract
from sentiment_classifier_pics import SentimentClassifier
import sentiment_classifier_pics as sc

def get_character_name(phrase):
	for sentence in nltk.sent_tokenize(phrase):
		all_upper = True
		for word in nltk.word_tokenize(sentence):
			if word == ".":
				continue
			if not word.isupper():
				all_upper = False
				break
		
		if all_upper:
			return sentence[:-1]
	return None


def order_phrases(extraction_file):
	phrases = extract(extraction_file)
	characters = {}
	dialogues = []

	for phrase in phrases:
		if phrase.startswith("SCENE") or phrase.startswith("ACT") or "END" in phrase:
			continue

		character_name = get_character_name(phrase)

		if character_name is not None:
			character_name = character_name.title()

			character_phrase = nltk.sent_tokenize(phrase)[1:]

			if character_name not in characters:
				gender = input("Which gender is %s? (male/female): " % character_name)
				characters[character_name] = gender
			
			dialogues.append((character_name, character_phrase))

	return characters, dialogues


def extract_relationship(extraction_file):
	characters, dialogues = order_phrases(extraction_file)
	print(characters)

	#with open("MultiNaiveBayesClassifier", "rb") as f:
	#	classifier = pickle.load(f)


	previous_speaker = None
	last_mentioned_entity = {"male": None, "female": None}
	relationship = []

	#result = open("result", "w")
	i = 1
	num_of_phrases = len(dialogues)
	for phrase in dialogues:
		speaker = phrase[0]
		entity = None
		attitude = None

		for sent in phrase[1]:
			word_tag = nltk.pos_tag(nltk.word_tokenize(sent))

			mother_tree = nltk.ne_chunk(word_tag)

			for tree in mother_tree:
				if hasattr(tree, 'label') and tree.label:
					if tree.label() == 'PERSON':
						entity_name = ' '.join([child[0] for child in tree])
						#print(entity_name)

						if entity_name.title() not in characters:
							continue

						last_mentioned_entity[characters[entity_name.title()]] = entity_name.title()
						entity = entity_name.title()

			for pair in word_tag:
				if pair[1] == "PRN":
					if pair[0].lower() in ("he", "him"):
						entity = last_mentioned_entity["male"]
					elif pair[0].lower() in ("she", "her"):
						entity = last_mentioned_entity["female"]

			#feat = sc.find_features(nltk.untag(word_tag))
			#attitude = classifier.classify(feat)
			color = sc.find_features(nltk.untag(word_tag))

			#result.write("Speaks: {}\nTo: {}\nAttitude: {}\nSaid: {}\n\n".format(speaker, entity, attitude, sent))
			#print("Speaks: {}\nTo: {}\nAttitude: {}\nSaid: {}\n\n".format(speaker, entity, attitude, sent))

		relationship.append((speaker, entity, color))

		print((i / num_of_phrases) * 100)

		i += 1

	return relationship
