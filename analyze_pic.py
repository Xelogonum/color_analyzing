import random
from PIL import Image, ImageColor, ImageDraw
from io import BytesIO
from math import sqrt

def get_average_color(pic):
	image = Image.open(pic)
	width = image.size[0]  
	height = image.size[1]  	
	pix = image.load()

	stats = {}

	r = g = b = 0

	for i in range(width):
		for j in range(height):
			try:
				r += pix[i,j][0]
				g += pix[i,j][1]
				b += pix[i,j][2]
			except TypeError:
				return -1

	r //= height*width
	g //= height*width
	b //= height*width

	#r = sum(pix[i,j][0] for i in range(width) for j in range(height)) // height*width

	# '#%02x%02x%02x' % (a, b, c) #converts rgb to hex

	return (r, g, b)

def get_average_color_quad(pic):
	image = Image.open(pic)
	width = image.size[0]  
	height = image.size[1]  	
	pix = image.load()

	r = g = b = 0

	for i in range(width):
		for j in range(height):
			try:
				r += pix[i,j][0] ** 2
				g += pix[i,j][1] ** 2
				b += pix[i,j][2] ** 2
			except TypeError:
				return -1

	r //= height*width
	g //= height*width
	b //= height*width

	r = int(sqrt(r))
	g = int(sqrt(g))
	b = int(sqrt(b))

	if r > 256:
		r = 256

	if g > 256:
		g = 256
		
	if b > 256:
		b = 256

	#r = sum(pix[i,j][0] for i in range(width) for j in range(height)) // height*width

	# '#%02x%02x%02x' % (a, b, c) #converts rgb to hex

	return (r, g, b)


def draw_color(path, color):
	image = Image.new("RGBA", (30,30), (0,0,0,0))

	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, 30, 30), color)

	del draw

	image.save(path, "PNG")

if __name__ == '__main__':
	print(get_average_color("temp.jpg"))
