from tkinter import *
from word_tone import text2color
from random import randrange
import pickle

with open("words2color_hash", "rb") as f:
	mapped = pickle.load(f)

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()

		self.canvas_height = 900
		self.canvas_width = 900
		self.create_widgets()

	def pressed_enter(self, e):
		text = self.text_entry.get()

		shift = 50
		if self.last_word is None:
			self.last_word = self.color_field.create_text(shift, shift, font=('Helvetica', '13'), text=" ")		

		for word in text.split(" "):
			x = self.color_field.bbox(self.last_word)[2]
			y = shift + 10 * (x // self.canvas_width)

			print(x, y)
			
			self.last_word = self.color_field.create_text(x, y, font=('Helvetica', '13'), text=word, fill="#%02x%02x%02x" % text2color(mapped, word))

	def create_widgets(self):
		self.color_field = Canvas(self, height=self.canvas_height, width=self.canvas_width)
		self.text_entry = Entry(font=('Helvetica', '13'))
		self.last_word = None
		
		self.color_field.grid()
		self.text_entry.grid(column=0, row=0, sticky=NW, columnspan=5)

		self.text_entry.bind('<Return>', self.pressed_enter)

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