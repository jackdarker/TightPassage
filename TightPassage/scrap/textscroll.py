#this is freely given, do what you will with it. Hope it's helpful :)

import pygame
import math
import src.Const as Const
import random
from pygame.locals import *

#setup

background_colour = (0,0,0)
(width, height) = (800, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Text based RPG')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

bg_image = pygame.image.load(Const.resource_path('assets\\cgs\\bg.png'))

#define the properties of a button
class button:
	def __init__(self, name, rectangle,colour, enabled):
		self.name = name
		self.rectangle = rectangle
		self.enabled = enabled
		self.colour = colour

header_text = "This is the header text which will not scroll"

body_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vel porta nibh. Cras auctor tortor vitae nulla molestie, at pulvinar libero aliquam. Donec ut magna fermentum, dapibus magna porttitor, suscipit ipsum. Aenean dapibus tortor id augue fringilla cursus. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nulla facilisi. Nunc suscipit ligula tincidunt accumsan rhoncus. Phasellus quis orci eget mi condimentum feugiat. Morbi a dui vel dolor convallis egestas eu id ante. In aliquam sem in ullamcorper placerat. Morbi convallis malesuada dictum. Nam tincidunt quis dolor nec posuere. Nam ut tempus lorem. Maecenas tempus tortor laoreet nisi lobortis, eu rhoncus lectus posuere. Nam risus nisl, mollis a rhoncus non, gravida vulputate diam. Cras accumsan turpis orci, non consequat purus aliquam eget. Pellentesque placerat dignissim risus ac egestas. Integer molestie nunc nec fermentum consequat. Nullam pellentesque congue ipsum, sed maximus sapien. Nullam consequat ultricies diam id molestie. Pellentesque iaculis tortor sagittis fermentum efficitur."

#define the buttons which can be on the screen, [name, x, y, size_x, size_y, enabled]
buttons = [
		button(">LOOK", [20, 400, 150, 50], [125,125,125], True),
		button(">TALK", [20, 500, 150, 50], [125,125,125], True),
		button(">INVENTORY", [300, 400, 150, 50], [125,125,125], True),
		button(">MAIN MENU", [250, 530, 150, 50], [125,125,125], True),
		button(">SAVE", [450, 530, 150, 50], [125,125,125], True)
	]

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rectangle, scroll):
	y = rectangle[1]
	lineSpacing = 2

	# get the height of the font
	fontHeight = myfont.size("Tg")[1]

	while text:
		i = 1

		# determine if the row of text will be outside our area
		if y + fontHeight > rectangle[1] + rectangle[3]:
			break

		# determine maximum width of line
		while myfont.size(text[:i])[0] < rectangle[2] and i < len(text):
			i += 1

		# if we've wrapped the text, then adjust the wrap to the last word      
		if i < len(text): 
			i = text.rfind(" ", 0, i) + 1

		if scroll > 0:
			scroll -= 1
		else:
			# render the line and blit it to the surface
			image = myfont.render(text[:i], True, color)

			surface.blit(image, (rectangle[0], y))
			y += fontHeight + lineSpacing

		# remove the text we just blitted
		text = text[i:]

	return text

	

#draw the text window at coordinates x,y
def draw():
	screen.blit(bg_image, (0,0))
	
	#draw the floating header
	text = myfont.render(header_text, True, [255,255,255])
	screen.blit(text, [20, 20])

	#draw the main text
	drawText(screen, body_text, [255,255,255], [20, 50, 550, 300], scroll)

	#draw the buttons
	for b in buttons:
		if b.enabled == True:
			pygame.draw.line(screen, b.colour, [b.rectangle[0], int(0.5*(2*b.rectangle[1] + b.rectangle[3]))], 
				[b.rectangle[0] + b.rectangle[2], int(0.5*(2*b.rectangle[1] + b.rectangle[3]))], b.rectangle[3])#
			text = myfont.render(b.name, True, [255,255,255])
			screen.blit(text, [b.rectangle[0] + 15, b.rectangle[1] + 15])


#for each button check if it was pressed
def getButton(mouse_pos):
	for b in buttons:
		if ((mouse_pos[0] > b.rectangle[0]) and
			(mouse_pos[0] < b.rectangle[0] + b.rectangle[2]) and
			(mouse_pos[1] > b.rectangle[1]) and
			(mouse_pos[1] < b.rectangle[1] + b.rectangle[3])):
			print("You clicked on button: ", b.name)
			return b.name


scroll = 0
running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	    elif event.type == pygame.MOUSEBUTTONDOWN:
	    	mouse_pos = pygame.mouse.get_pos()	
	    	#left click
	    	if event.button == 1:
	    		button_name = getButton(mouse_pos)
	    	#scroll wheel
	    	if event.button == 4:
	    		if scroll > 0:
	    			scroll -= 1
	    	if event.button == 5:
	    		if scroll < 20:
	    			scroll += 1
	       

	screen.fill(background_colour)

	draw()

	pygame.display.flip()
	
	

pygame.quit()
