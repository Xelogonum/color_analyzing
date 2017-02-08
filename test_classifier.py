from sentiment_classifier_pics import SentimentClassifier
import pickle, json
import sentiment_classifier_pics as sc
import urllib.request as rq
from urllib.parse import urlencode
from time import sleep

token = "60e47cef337773c269e3f115e6b0e7bb8fddd9f8585d52548b48c245bfa8f6e4875fe2296064fe2c5d1ce"
prev = ""

with open("MultiNaiveBayesClassifier", "rb") as file:
	classifier = pickle.load(file)

def give_label(text):
	result = sc.find_features(text.split(" "))
	print((result["r"], result["g"], result["b"]))
	print(result)
	mark = classifier.classify()
	if mark == "pos":
		return "Positive"
	else: 
		return "Negative"

def message(text):
	#https://oauth.vk.com/authorize?client_id=5178322&redirect_uri=https://oauth.vk.com/blank.html&scope=messages&response_type=token&v=5.60
	
	url = "https://api.vk.com/method/messages.send?"
	answer = rq.urlopen(url, urlencode({"chat_id": 17, "message": text, "access_token": token, "v": 5.60}).encode("utf-8"))

def listen():
	global prev
	url = "https://api.vk.com/method/messages.get?"
	answer = rq.urlopen(url, urlencode({"count": 1, "filter": 0, "access_token": token}).encode("utf-8"))

	parsed_string = json.loads(answer.read().decode("utf-8"))
	string = parsed_string["response"][1]["body"]
	if parsed_string["response"][1]["title"] == 'НИИ "Прон, арты, бомбежки"' and string.startswith("!") and prev != string:
		message(give_label(string[1:]))
		prev = string

while True:
	print(give_label(input("Enter: ").lower()))