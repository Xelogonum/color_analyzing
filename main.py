import nltk
from analyzer import extract_relationship
from sentiment_classifier_pics import SentimentClassifier

summary = {}
#TheSchoolforScandal.html
relationship_list = extract_relationship("TheSchoolforScandal.html")

for relation in relationship_list:
	summary.setdefault(relation[0], {})

	summary[relation[0]].setdefault(relation[1], [])

	summary[relation[0]][relation[1]].append(relation[2])

print(summary)
with open("log", "w") as f:
	f.write(str(summary))