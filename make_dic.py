import pickle
import urllib
import urllib.request as rq
from urllib.parse import urlencode
from nltk.corpus import movie_reviews
from time import sleep
from word_tone import word_color

def message(text):
	token = "60e47cef337773c269e3f115e6b0e7bb8fddd9f8585d52548b48c245bfa8f6e4875fe2296064fe2c5d1ce"
	#https://oauth.vk.com/authorize?client_id=5178322&redirect_uri=https://oauth.vk.com/blank.html&scope=messages&response_type=token&v=5.60
	
	url = "https://api.vk.com/method/messages.send?"
	urllib.request.urlopen(url, urlencode({"user_id": 212285182, "message": text, "access_token": token}).encode("utf-8"))

def main():
	with open("words2color_hash", "rb") as f:
		mapped = pickle.load(f)

	i = 1
	big_er_counter = 0
	for word in set(movie_reviews.words()):
		print("# %d " % i, end="")

		i += 1

		if word in mapped:
			print(word + " already in")
			continue

		for j in range(5):
			try:
				mapped[word] = word_color(word)
				print(word + " added")
				break
			except (urllib.error.URLError, urllib.error.HTTPError):
				message("BEDA")
				print("error")
				sleep(10)
			except:
				message("DANILA BLYAT PIZDEC")
				print("BIG ERROR")
				big_er_counter += 1
				break

		if big_er_counter > 14:
			message("POLEGLO VSE SUKA")
			print("Something went wrong...\nFinishing")
			break

		if i % 1000 == 0:
			message("Completed: %f" % ((i / 39768) * 100))
			with open("words2color_hash", "wb") as f:
				pickle.dump(mapped, f)
		

	with open("words2color_hash", "wb") as f:
		pickle.dump(mapped, f)

if __name__ == '__main__':
	main()