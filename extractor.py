from html.parser import HTMLParser

"""Extracts characters phrases from given HTML file."""

class Parser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.phrases = []

	def handle_data(self, data):
		data = data.replace("\n    ", "").strip()
		if len(data) > 0:
			self.phrases.append(data)

parser = Parser()

def extract(file):
	with open(file, "r") as source:
		parser.feed(source.read())

	return parser.phrases
