import urllib
import urllib.request as rq
import analyze_pic as ap
import nltk
import colorsys
from bs4 import BeautifulSoup
from math import sqrt

def download_pic(query, num_samples=7):

	url = "https://www.google.ru/search?q=" + query + "&source=lnms&tbm=isch&gws_rd=ssl"
	#url = "https://stock.adobe.com/search?k=" + query + "&show_images=1"

	rq_obj = rq.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"})
	soup = BeautifulSoup(rq.urlopen(rq_obj), 'html.parser')

	links = soup.find_all("img")
 
	return [i["src"] for i in links[1:num_samples+1]]

def word_color_weighted(word):

	r = g = b = 0
	weight = 0

	analyzed = 0
	for url in download_pic(word):
		picture, headers = rq.urlretrieve(url)

		color = ap.get_average_color(picture)

		if color == -1:
			continue

		hls_color = colorsys.rgb_to_hls(color[0]/255, color[1]/255, color[2]/255) #hue, lightness, sturation

		r += color[0] * hls_color[2]
		g += color[1] * hls_color[2]
		b += color[2] * hls_color[2]

		weight += hls_color[2]
		analyzed += 1
		ap.draw_color("./colors/"+str(analyzed) + "_weighted", (int(color[0] * hls_color[2]), int(color[1] * hls_color[2]), int(color[2] * hls_color[2])))

	r //= weight
	g //= weight
	b //= weight
	ap.draw_color("./colors/"+word+"_weighted", (int(r), int(g), int(b)))

	return (r, g, b)
	
def word_color(word):

	r = g = b = 0

	analyzed = 1
	for url in download_pic(word):
		picture, headers = rq.urlretrieve(url)

		color = ap.get_average_color(picture)

		if color == -1:
			continue

		r += color[0]
		g += color[1]
		b += color[2]

		analyzed += 1
		ap.draw_color("./colors/"+str(analyzed), (color[0], color[1], color[2]))

	r //= analyzed
	g //= analyzed
	b //= analyzed
	ap.draw_color("./colors/"+word+"_norm", (r, g, b))

	return (r, g, b)
	
def text2color(wc_table, text):
	r = g = b = 0

	if type(text) != type([]):
		text = nltk.word_tokenize(text)

	text_length = len(text)

	for pair in nltk.pos_tag(text, tagset='universal'):
		#print(pair)
		if pair[1] in ("PRON", "ADP", "CONJ", "PRT"):
			text_length -= 1
			continue
		
		if pair[0] not in wc_table:
			try:
				new_word = word_color_weighted(pair[0].lower())
				r += new_word[0]
				g += new_word[1]
				b += new_word[2]
				#print("{}: {}".format(word, new_word))
				continue
			except:
				text_length -= 1
				continue

		r += wc_table[pair[0].lower()][0]
		g += wc_table[pair[0].lower()][1]
		b += wc_table[pair[0].lower()][2]

	if text_length <= 0:
		text_length = 1

	r //= text_length
	g //= text_length
	b //= text_length

	#ap.draw_color("./"+"_".join(text[:4])+"2", (r, g, b))

	return (r, g, b)

if __name__ == '__main__':
	for word in ("luck", "hate", "love", "happiness", "like"):
		word_color(word)
		word_color_weighted(word)