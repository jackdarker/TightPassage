"""<title>an example of layout usage</title>"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")
import src.Const as Const
from src.UI.pgu.pgu.gui import layout
from src.UI.pgu.pgu import gui

pygame.font.init()

screen = pygame.display.set_mode((420,320),SWSURFACE)
bg = (255,255,255)
fg = (0,0,0)
screen.fill(bg)

class Obj: pass

l = layout.Layout(pygame.Rect(0,0,320,320))

e = Obj()
_img = pygame.Surface((30,30))
_img.fill(Const.YELLOW)
e.image = _img
#e.image = pygame.image.load("cuzco.png")
e.rect = pygame.Rect(0,0,e.image.get_width(),e.image.get_height())
e.align = -1
l.add(e) #aligned object
l.add((0,50)) #br
e = Obj()
_img = pygame.Surface((30,30))
_img.fill(Const.RED)
e.image = _img
e.rect = pygame.Rect(0,0,e.image.get_width(),e.image.get_height())
e.align = 1
l.add(e) #aligned object
for i in range(0,5):
    e = Obj()
    _img = pygame.Surface((30,30))
    _img.fill(Const.GREEN)
    bt = gui.Button(str(i))
    bt.resize(width=100,height=50)  #doesnt work with buttons??
    #bt.rect=bt.value.rect.copy()
    #e.rect = pygame.Rect(0,0,bt.get_width(),bt.get_height())
    #e.align = 0
    #l.add(bt) #aligned object
font = pygame.font.SysFont("default", 24)

w,h = font.size(" ")
l.add((0,50)) #br
l.add(-1) #start of new block

for word in """Welcome to my little demo of the layout module. The demo does not do a whole lot, but I'm sure you will be very impressed by it. blah blah blah. The demo does not do a whole lot, but I'm sure you will be very impressed by it. blah blah blah.""".split(" "):
    e = Obj()
    e.image = font.render(word,1,fg)
    e.rect = pygame.Rect(0,0,e.image.get_width(),e.image.get_height())
    l.add(e) #inline object
    l.add((w,h)) #space

##The layout object will layout words, and document elements for you
##::
l.add(-1) #start of new block
for word in """The demo does not do a whole lot, but I'm sure you will be very impressed by it. blah blah blah. The demo does not do a whole lot, but I'm sure you will be very impressed by it. .""".split(" "):
    e = Obj()
    e.image = font.render(word,1,fg)
    e.rect = pygame.Rect(0,0,e.image.get_width(),e.image.get_height())
    l.add(e) #inline object
    l.add((w,h)) #space
##

l.resize()

for e in l.widgets:
    #e.paint(screen)
    screen.blit(e.image,(e.rect.x,e.rect.y))
    
pygame.display.flip()

_quit = 0
while not _quit:
    for e in pygame.event.get():
        if e.type is QUIT: _quit = 1
    pygame.time.wait(10)
