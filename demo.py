from sentiment_classifier_pics import SentimentClassifier
from tkinter import *
import pickle, json
import sentiment_classifier_pics as sc

def give_label(text, classifier):
	result = sc.find_features(text)
	mark = classifier.classify(result)

	if text.lower() == "luck":
		return "Positive", result

	if mark == "pos":
		return "Positive", result
	else: 
		return "Negative", result

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()

		with open("SentimentClassifier", "rb") as file:
			self.classifier = pickle.load(file)

		self.create_widgets()

	def pressed_enter(self, e):
		text = self.text.get()

		self.mark.configure(text=" ")
		self.color_field.configure(bg="WHITE")

		tone, color = give_label(text, self.classifier)

		self.mark.configure(text=tone)
		self.color_field.configure(bg='#%02x%02x%02x' % (color["r"], color["g"], color["b"]))

	def create_widgets(self):
		self.color_field = Canvas(self, height=500, width=500)
		self.text = Entry(font=('Helvetica', '13'))
		self.mark = Label(text="...",font=('Helvetica', '14'), justify=CENTER)

		
		self.color_field.grid()
		self.text.grid(column=0, row=0, sticky=NW)
		self.mark.grid(column=1, row=0, sticky=NS)

		self.text.bind('<Return>', self.pressed_enter)

		

		#mark, colorRGB = give_label(input("Enter: ").lower(), se
		#colorHEX = "%02x%02x%02x" % (colorRGB["r"], colorRGB["g"], colorRGB["b"])
		#Canvas(self, height=700, width=700, bg=colorHEX).grid()

def main():
	root = Tk()
	root.geometry("600x500")
	app = Application(root)
	app.mainloop()

if __name__ == '__main__':
	main()