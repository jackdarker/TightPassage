"""<title>Integration with a Game</title>
For games, it is usually preferrable to not have your game within
a GUI framework.  This GUI framework can be placed within your game.
"""

import time
import random
import pygame
from pygame.locals import *
import src.Const as Const

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from src.UI.pgu.pgu import gui
#from gui7 import ColorDialog

# The maximum frame-rate
FPS = 30
WIDTH,HEIGHT = 640,480

##You can initialize the screen yourself.
##::
screen = pygame.display.set_mode((640,480),SWSURFACE)
##
class ColorDialog(gui.Dialog):
    def __init__(self,value,**params):
        self.value = list(gui.parse_color(value))
        
        title = gui.Label("Color Picker")
        
        main = gui.Table()
        
        main.tr()
        
        self.color = gui.Color(self.value,width=64,height=64)
        main.td(self.color,rowspan=3,colspan=1)
        
        ##The sliders CHANGE events are connected to the adjust method.  The 
        ##adjust method updates the proper color component based on the value
        ##passed to the method.
        ##::
        main.td(gui.Label(' Red: '),1,0)
        e = gui.HSlider(value=self.value[0],min=0,max=255,size=32,width=128,height=16)
        e.connect(gui.CHANGE,self.adjust,(0,e))
        main.td(e,2,0)
        ##

        main.td(gui.Label(' Green: '),1,1)
        e = gui.HSlider(value=self.value[1],min=0,max=255,size=32,width=128,height=16)
        e.connect(gui.CHANGE,self.adjust,(1,e))
        main.td(e,2,1)

        main.td(gui.Label(' Blue: '),1,2)
        e = gui.HSlider(value=self.value[2],min=0,max=255,size=32,width=128,height=16)
        e.connect(gui.CHANGE,self.adjust,(2,e))
        main.td(e,2,2)
                        
        gui.Dialog.__init__(self,title,main)
        
    ##The custom adjust handler.
    ##::
    def adjust(self,value):
        (num, slider) = value
        self.value[num] = slider.value
        self.color.repaint()
        self.send(gui.CHANGE)
    ##

class IconButton(gui.Button):
    def __init__(self,value=None,**params):
        super(IconButton, self).__init__(value,**params)
        self.value.style.align=1 

        #possibility to define own ctrls with theme:
        #params.setdefault('cls', 'iconbutton')
        #super(gui.Button, self).__init__(**params)
        #self.value = value
        self.minWidth =200
        self.icon = pygame.Surface((30,30))
        self.icon.fill(Const.YELLOW)

    def paint(self,s):
        rect = self.value.rect
        if (self.pcls == "down"):
            # Shift the contents down to emphasize the button being pressed. This
            # is defined in the theme config file.
            rect = rect.move((self.style.down_offset_x, self.style.down_offset_y))
        self.value.pcls = self.pcls

        self.value.paint(gui.surface.subsurface(s, rect))
        s.blit(self.icon,(5,5))

    def resize(self,width=None,height=None):
        # Calculate the size of the rendered text
        (self.style.width, self.style.height) = self.value.font.size(self.value.value)
        self.style.width+=50
        self.style.height+=20
        self.style.width = max(self.style.width,self.minWidth)

        self.value.rect.x,self.value.rect.y = 0,0
        self.value.rect.w,self.value.rect.h = self.value.resize(self.style.width,self.style.height)
        return self.value.rect.w,self.value.rect.h

class ListControl2(gui.List):
    """...using List"""
    def __init__(self, width, height, **params):
        super(ListControl2, self).__init__(width, height, **params)
        bt = IconButton("Clickdfsdgffdgdgf 1 Me!")
        self.add(bt)
        bt = IconButton("Click  2 Me!")
        self.add(bt)

def resizeMe(bt,_event,_widget):    #_event & _widget see widget.connect details
    _
    pass

class ListControl(gui.Table):
    """...using a table"""
    def __init__(self,**params):
        gui.Table.__init__(self,**params)

        fg = (255,255,255)

        self.tr()
        self.td(gui.Label("My List",color=Const.YELLOW),colspan=2)

        self.tr()
        bt = IconButton("Clickdfsdgffdgdgf 1 Me!")
        bt.connect(gui.KEYDOWN, resizeMe, bt)
        self.td(bt,align=-1)
        self.tr()
        bt = IconButton("Click  2 Me!")
        bt.connect(gui.CLICK, resizeMe, bt)
        self.td(bt,align=-1)
        self.tr()
        bt = IconButton("Click      3 Me!")
        bt.connect(gui.CLICK, resizeMe,bt)
        self.td(bt,align=-1)



class ListControl3(gui.ScrollArea):
    """...using a table in scrollarea"""
    def __init__(self,**params):
        self.table = gui.Table(**params)
        gui.ScrollArea.__init__(self,self.table,height=200,width=200,**params)

        fg = (255,255,255)

        self.table.tr()
        self.table.td(gui.Label("My List",color=Const.YELLOW),colspan=2)

        self.table.tr()
        bt = IconButton("Clickdfsdgffdgdgf 1 Me!")
        #bt.connect(gui.CLICK, resizeMe, bt)
        self.table.td(bt,align=-1)
        self.table.tr()
        bt = IconButton("Click  2 Me!")
        self.table.td(bt,align=-1)
        self.table.tr()
        bt = IconButton("Click      3 Me!")
        self.table.td(bt,align=-1)
    
    def event(self,e):
        used = False
        used = super().event(e)
        return used

class StarControl(gui.Table):
    def __init__(self,**params):
        gui.Table.__init__(self,**params)

        def fullscreen_changed(btn):
            #pygame.display.toggle_fullscreen()
            print("TOGGLE FULLSCREEN")
        
        def resizeMe(btn):
            btn.resize(50,100)

        def stars_changed(slider):
            n = slider.value - len(stars)
            if n < 0:
                for i in range(n,0): 
                    stars.pop()
            else:
                for i in range(0,n):
                    stars.append([random.randrange(-WIDTH*span,WIDTH*span),
                                  random.randrange(-HEIGHT*span,HEIGHT*span),
                                  random.randrange(1,dist)])

        fg = (255,255,255)

        self.tr()
        self.td(gui.Label("Phil's Pygame GUI",color=fg),colspan=2)
        
        self.tr()
        self.td(gui.Label("Speed: ",color=fg),align=1)
        e = gui.HSlider(100,-500,500,size=20,width=100,height=16,name='speed')
        self.td(e)
        
        self.tr()
        self.td(gui.Label("Size: ",color=fg),align=1)
        e = gui.HSlider(2,1,5,size=20,width=100,height=16,name='size')
        self.td(e)
        
        self.tr()
        self.td(gui.Label("Quantity: ",color=fg),align=1)
        e = gui.HSlider(100,1,1000,size=20,width=100,height=16,name='quantity')
        e.connect(gui.CHANGE, stars_changed, e)
        self.td(e)
        
        self.tr()
        self.td(gui.Label("Color: ",color=fg),align=1)
        
        
        default = "#ffffff"
        color = gui.Color(default,width=64,height=10,name='color')
        color_d = ColorDialog(default)

        color.connect(gui.CLICK,color_d.open,None)
        self.td(color)
        def update_col():
            color.value = color_d.value
        color_d.connect(gui.CHANGE,update_col)
        
        btn = gui.Switch(value=False,name='fullscreen')
        btn.connect(gui.CHANGE, fullscreen_changed, btn)

        self.tr()
        self.td(gui.Label("Full Screen: ",color=fg),align=1)
        self.td(btn)
        
        self.tr()
        self.td(gui.Label("Warp Speed: ",color=fg),align=1)
        self.td(gui.Switch(value=False,name='warp'))

##Using App instead of Desktop removes the GUI background.  Note the call to app.init()
##::

form = gui.Form()
themetouse = ("default") #themetouse = Const.resource_path("assets/pgu_themes/yellow")
app = gui.App(theme=gui.Theme(themetouse))
starCtrl = StarControl()
listCtrl = ListControl()#(200,200)
listCtrl3 = ListControl3()#200,200)
c = gui.Container(align=-1,valign=-1)
c.add(starCtrl,0,0)
c.add(listCtrl3,50,250)
c.add(listCtrl,330,250)

app.init(c)
##

dist = 8192
span = 10
stars = []
def reset():
    global stars
    stars = []
    for i in range(0,form['quantity'].value):
        stars.append([random.randrange(-WIDTH*span,WIDTH*span),
                      random.randrange(-HEIGHT*span,HEIGHT*span),
                      random.randrange(1,dist)])
        

def render(dt):
    speed = form['speed'].value*10
    size = form['size'].value
    color = form['color'].value
    warp = form['warp'].value

    colors = []
    for i in range(256,0,-1):
        colors.append((color[0]*i/256,color[1]*i/256,color[2]*i/256))
        
    n = 0
    for x,y,z in stars:
        if warp:
            z1 = max(1,z + speed*2)
            x1 = x*256/z1
            y1 = y*256/z1
            xx1,yy1 = x1+WIDTH/2,y1+HEIGHT/2
    
        x = x*256/z
        y = y*256/z
        xx,yy = x+WIDTH/2,y+HEIGHT/2
        c = min(255,z * 255 / dist)
        col = colors[int(c)]

        if warp:
            pygame.draw.line(screen,col,
                             (int(xx1),int(yy1)),
                             (int(xx),int(yy)),size)
        
        pygame.draw.circle(screen,col,(int(xx),int(yy)),size)
        
        ch = 0
        z -= speed*min(0.5,dt)
        if z <= 0: 
            ch = 1
            z += dist
        if z > dist: 
            ch = 1
            z -= dist
        if ch:
            stars[n][0] = random.randrange(-WIDTH*span,WIDTH*span)
            stars[n][1] = random.randrange(-HEIGHT*span,HEIGHT*span)
        stars[n][2] = z
        
        n += 1
        

##You can include your own run loop.
##::
reset()
clock = pygame.time.Clock()
done = False
while not done:
    for e in pygame.event.get():
        if e.type is QUIT: 
            done = True
        elif e.type is KEYDOWN and e.key == K_ESCAPE: 
            done = True
        else:
            app.event(e)

    # Clear the screen and render the stars
    dt = clock.tick(FPS)/1000.0
    screen.fill((0,0,0))
    render(dt)
    app.paint()
    pygame.display.flip()
