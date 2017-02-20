from tkinter import *
from word_tone import text2color
from random import randrange
import pickle

#TO USE PRECOLORIZED WORDS
with open("words2color_hash", "rb") as f:
	mapped = pickle.load(f)

#mapped = {}

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()

		self.canvas_height = 900
		self.canvas_width = 900
		self.create_widgets()
		self.default_font = ('Helvetica', '13', 'bold')

	def pressed_enter(self, e):
		text = self.text_entry.get()

		xshift = 20
		yshift = 50
		line_spacing = 20
		word_spacing = 3

		if self.last_word is None:
			self.last_word = self.color_field.create_text(xshift, yshift, font=self.default_font, text="")		

		for word in text.split(" "):
			word = word.strip("\n")

			temp = self.color_field.create_text(0, 0, font=self.default_font, text=word)
			word_width = self.color_field.bbox(temp)[2] - self.color_field.bbox(temp)[0]
			print(word_width)
			self.color_field.delete(temp)

			x = self.color_field.bbox(self.last_word)[2] + word_width//2 + word_spacing
			y = (self.color_field.bbox(self.last_word)[3] + self.color_field.bbox(self.last_word)[1]) // 2

			self.last_word = self.color_field.create_text(x, y, font=self.default_font, text=word, fill="#%02x%02x%02x" % text2color(mapped, word))

			if self.color_field.bbox(self.last_word)[2] > self.canvas_width:
				self.color_field.delete(self.last_word)

				x = xshift
				y += line_spacing

				self.last_word = self.color_field.create_text(x, y, font=self.default_font, text=word, fill="#%02x%02x%02x" % text2color(mapped, word))

	def clear_text(self, e):
		for word in self.color_field.find_all():
			self.color_field.delete(word)
		self.last_word = None

	def create_widgets(self):
		self.color_field = Canvas(self, height=self.canvas_height, width=self.canvas_width, bg="WHITE")
		self.text_entry = Entry(font=('Helvetica', '13'))
		self.last_word = None
		
		self.color_field.grid()
		self.text_entry.grid(column=0, row=0, sticky=NW, columnspan=5)

		self.text_entry.bind("<Return>", self.pressed_enter)
		self.text_entry.bind("<Control-r>", self.clear_text)

		#mark, colorRGB = give_label(input("Enter: ").lower(), se
		#colorHEX = "%02x%02x%02x" % (colorRGB["r"], colorRGB["g"], colorRGB["b"])
		#Canvas(self, height=700, width=700, bg=colorHEX).grid()

def main():
	root = Tk()
	root.geometry("901x901")
	app = Application(root)
	app.mainloop()

if __name__ == '__main__':
	main()