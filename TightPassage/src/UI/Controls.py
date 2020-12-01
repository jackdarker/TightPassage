import pygame
import time
import random
from pygame.locals import *
import src.Const as Const
from src.UI.pgu.pgu import gui
from src.UI.pgu.pgu import text
from src.UI.pgu.pgu import html
from src.UI.pgu.pgu.gui import pguglobals
import src.Components.ComponentGraphics

class IconButton(gui.Button):
    """a button with a icon
    """
    def __init__(self,value=None,**params):
        params.setdefault('minWidth',0)
        super(IconButton, self).__init__(value,**params)
        self.value.style.align=1 

        #possibility to define own ctrls with theme:
        #params.setdefault('cls', 'iconbutton')
        #super(gui.Button, self).__init__(**params)
        #self.value = value
        self.minWidth =params['minWidth']
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

class Tabsheet(gui.Container):
    """creates a tabsheetlike control because there is none in pgu
    """
    def __init__(self,tabContent={}, tabPosition=0,**params):
        """ tabcontent = dictionary where value is a widget and key is a string with the name of the tabpage
            tabPosition = where are the labels positioned in relation of the content (top,right,left,bottom)
            content area will resize according the widget-size; to avoid this set the widgets w.style.width and .height
        """
        super(Tabsheet, self).__init__(**params)
        
        #creates a tab; buttons are used to switch tabs
        self.tabs = gui.Group()
        self.tabs.connect(gui.CHANGE,self._switchTab)
        tablabels = gui.Table()
        tablabels.tr()
        #when the toolbutton is pressed it will call gui.CHANGE->tab() and this will switchout the boxwidget with tabcontent[x]
        noPages= 0
        pageSize = (0,0)
        self.tabContent = tabContent
        for tab in tabContent:
            noPages +=1
            pageSize = (max(pageSize[0],tabContent[tab].style.width), max(pageSize[1],tabContent[tab].style.height))
            b = gui.Tool(self.tabs,gui.Label(tab),tabContent[tab])#assign the toolbutton to the group, this will connect to the groups gui.CHANGE event
            tablabels.td(b)
            tablabels.tr()

        bt = gui.Button("V")
        tablabels.add(bt)
        noPages +=1
        bt.connect(gui.CLICK, self.toggle_expand)
       
        #the following widget will be switched out when pressing on the tablabels
        spacer = gui.Spacer(pageSize[0],pageSize[1])
        self.box = gui.ScrollArea(spacer,height=spacer.rect[1])
        tablabels.td(self.box,row=0,col=1,style={'border':1},rowspan=noPages)
        tablabels.tr()
        self.add(tablabels,0,0)
        self.is_expanded = True
        for key in tabContent.keys():
            self.switch_tab(key)
            break


    #function called when clicking tablabels to switch tab
    def _switchTab(self):
        self.box.widget = self.tabs.value

    def switch_tab(self,label):
        """ IMPORTANT: when tabcontent is a table where you add elements dynamical,
        you have to call table.resize() or get errors because of 0-size surfaces !?
        """
        self.box.widget =self.tabContent[label]

    def toggle_expand(self):
        #todo when not expanded only the expand-button will be visible
        if(self.is_expanded):
            #self.style.height=self.doc.style.height=self.scrollList.style.height= self.minScrollHeight
            pass
        else:
            #self.style.height=self.doc.style.height=self.scrollList.style.height= self.maxScrollHeight
            pass
        self.is_expanded = not self.is_expanded
        #self.scrollList.chsize()
        #self.doc.chsize() 
        #self.chsize()

class Textlog(gui.Container):
    """a scrollable textbox that can be toggled between small and big size
    width and height should be set and define the maximum area
    """
    def __init__(self,**params):
        super(Textlog,self).__init__(**params)
        self.layout = gui.Table()
        textWidth=scrollWidth=0
        self.linecount =0
        if('width' in params):
            textWidth = params['width']-50
            scrollWidth = textWidth
        
        self.maxScrollHeight =0
        if('height' in params):
            self.maxScrollHeight = params['height']
        
        self.doc = gui.TextArea(value="",focusable=True,editable=True,width=textWidth,height=self.maxScrollHeight,align=-1,valign=-1)#gui.Document(width=textWidth,align=-1,valign=-1)
        self.scrollList = gui.ScrollArea(self.doc,width=scrollWidth,height=self.maxScrollHeight,hscrollbar=False, vscrollbar=True)
        space = self.doc.style.font.size(" ")
        self.minScrollHeight = space[1] #at least 1 line visible
        self.font = pygame.font.SysFont("sans", 16)     #todo styling
        #self.doc.block(align=-1)

        self.layout.tr()
        self.layout.add(self.scrollList,col=0,row=0,rowspan=5)
        #resize button
        bt = gui.Button('V')
        bt.connect(gui.CLICK, self.toggle_expand)
        self.layout.add(bt,col=1,row=0)
        #clear button
        bt = gui.Button('C')
        bt.connect(gui.CLICK, self.clear_text)
        self.layout.add(bt,col=1,row=4)
        self.add(self.layout,0,0)
        #minimize on start
        self.is_expanded=True
        self.toggle_expand()
        #self.set_text('Cuzcos Paint is a revolutionary new paint program it has all the awesome features that you need to paint really great pictures.')
        

    def add_text(self,text):
        self.linecount +=1
        if(self.linecount>20):
            self.doc.value =""
            self.linecount=0
        self.doc.value +="""\n""" + text
        self.scrollList.set_vertical_scroll(65535)  #scrolls automat. to end of list
        return  #todo if adding each word to document as label, this will cause huge FPS drop
        #Textarea on opposite doesnt resize to textsize and therfore doestn make use of scrollbars ?!
        #self.doc.remove_all()
        space = self.font.size(" ")
        self.doc.br(space[1])
        for word in text.split(" "): 
            self.doc.add(gui.Label(word))
            self.doc.space(space)
        
        self.scrollList.set_vertical_scroll(65535)  #scrolls automat. to end of list

    def clear_text(self):
        self.doc.value =""
        return
        self.doc.remove_all()
        #add at least space or area shrinks to 0
        space = self.font.size(" ")
        self.doc.br(space[1])

    def toggle_expand(self):
        if(self.is_expanded):
            self.style.height=self.doc.style.height=self.scrollList.style.height= self.minScrollHeight
            pass
        else:
            self.style.height=self.doc.style.height=self.scrollList.style.height= self.maxScrollHeight
            self.doc.vscroll = 0
            pass
        self.is_expanded = not self.is_expanded
        self.scrollList.chsize()
        self.doc.chsize() 
        self.chsize()

class PercentBar(pygame.sprite.Sprite):
    """similiar to Progressbar but with change of color depending actual value
        gradient is list of tuples (threshold,color); the color will be active if value>=threshold;
        there should be at least listitems for value = min and =max

    """
    def __init__(self, size, gradient, horizontal=True):
        self.gradient = gradient
        self.color = gradient[0][1]
        pygame.sprite.Sprite.__init__(self)
        self.percent = self.old_percent = self.ani_percent = 1.0
        self.ani_speed = Const.FPS*0.1
        self.horizontal = horizontal
        self.image = pygame.Surface(size).convert_alpha()
        self.rect = self.image.get_rect()

    def set_percent(self, value):
        """value is [0.00..1.00]
        """
        self.ani_percent = 0.0
        self.old_percent = self.percent
        self.percent = value
        if(self.percent<0): self.percent=0
        for grad in self.gradient:
            if(self.percent>=grad[0]):
                self.color=grad[1]

    def draw(self, surface):
        # Render to the screen
        surface.blit(self.image, self.rect.topleft)

    def update(self,dt):
        #after value was changed animate the change
        #
        if(self.percent != self.old_percent):
            self.ani_percent = self.ani_percent +self.ani_speed/100
            if(self.ani_percent>1): 
                self.ani_percent =1

            y = height = old_height = self.rect.h
            x = width = old_width = self.rect.w
            if self.horizontal:     #todo also in right to left direction
                #width = round(self.rect.w * self.percent)
                old_width = round(self.rect.w * self.old_percent)
                width = round(self.rect.w * self.ani_percent* (self.old_percent - self.percent))
                x = old_width - width
            else:
                old_height = round(self.rect.h * self.old_percent)
                height = round(self.rect.h * self.ani_percent* (self.old_percent - self.percent))
                y = old_height - height

            self.image.fill(Const.OPAGUE)
            if(self.ani_percent>=1):
                self.old_percent = self.percent
                pygame.draw.rect(self.image,self.color,(0, 0, x, y))
            else:
                if self.horizontal:
                    y = 0
                else:
                    x = 0
                pygame.draw.rect(self.image,self.color,(0, 0, old_width, old_height))
                pygame.draw.rect(self.image,Const.BRIGHT_RED,(x, y, width, height)) #todo color= complement color
            pygame.draw.rect(self.image,Const.BLACK,self.rect,1) #draw border

        pass

class ColorBar(gui.ProgressBar):
    """similiar to Progressbar but with change of color depending actual value
        gradient is list of tuples (threshold,color); the color will be active if value>=threshold
        there should be at least listitems for value = min and =max
    """
    def __init__(self,value,min,max,gradient,**params):
        self.gradient = gradient
        self.color = gradient[0][1]
        super(ColorBar,self).__init__(value,min,max,**params)
        
    #@property
    #def value(self):
    #    return super(ColorBar,self).value

    @gui.ProgressBar.value.setter
    def value(self, val):
        for grad in self.gradient:
            if(val>=grad[0]):
                self.color=grad[1]
        #wtf: cannot call super().value=val; instead i have to use invisible functions fset,fget,fdel to reroute call
        gui.ProgressBar.value.fset(self, val)


    def paint(self,s):
        if (self.value != None):
            r = pygame.rect.Rect(0,0,self.rect.w,self.rect.h)
            r.w = r.w*(self.value-self.min)/(self.max-self.min)
            self.bar = r
            pguglobals.app.theme.render(s,self.color,r)
        pass

class CharacterCard(gui.Container):
    """displays the actual character-bust and stats
    """
    def __init__(self, **params):
        #Todo by default container dont have backgrounds so we assign a Image here
        params['background'] = pygame.image.load(Const.resource_path("assets/pgu_themes/game/dialog.png")) #src.Const.WHITE  
        super(CharacterCard,self).__init__(**params)
        #self.layout = gui.Table()
        #self.layout.style.width=250
        #self.layout.style.height=200
        self.style.width=250
        self.style.height=200
        self.char=None
        self.dirty = True
        icon = pygame.Surface((64,64)).convert_alpha()
        icon.fill(Const.RED)
        self.Bust = gui.Image(icon)
        self.Name = gui.Label("???")
        #self.layout.tr()
        #self.layout.add(self.Bust,col=0,row=0,rowspan=2,colspan=5)
        self.Healthbar = ColorBar(10,0,100,[(0,Const.RED),(20,Const.YELLOW),(50,Const.GREEN)],width=100)
        #self.layout.tr()
        #self.layout.add(self.Healthbar,col=1,row=6)
        self.Staminabar = gui.ProgressBar(50,0,100,width=100)
        #self.layout.tr()
        #self.layout.add(self.Healthbar2,col=1,row=7)

        def myfnc(target):
            #target.value+=1
            pass
        self.Bust.connect(gui.CLICK,myfnc,self.Healthbar)
        #self.add(self.layout,0,0)
        self.add(self.Name,10,10)
        self.add(self.Bust,10,30)
        self.add(self.Healthbar,100,10)
        self.add(self.Staminabar,100,40)

    #def draw(self, surface):
        # Render to the screen
     #   surface.blit(self.Frame, (0,0))
     #   surface.blit(self.Bust, (0,0))
     #   self.Healthbar.draw(surface)

    def set_char(self,char):
        """connects the card with a character"""
        self.char=char
        self.dirty = True

    def update(self,s): 
        #this is not an override from gui.Container - because we dont use gui.desktop no update is called
        if (self.dirty and self.char != None):
            self.Name.set_text(self.char.name)
            self.Bust.value = self.char.get_portrait()
            self.Healthbar.value = self.char.HP*100 / self.char.MaxHP
        self.dirty = False
        pass


def renderTextCenteredAt(text, font, colour, x, y, screen, allowed_width):
    # first, split the text into words
    words = text.split()

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    # now we've split our text into lines that fit into the width, actually
    # render them

    # we'll render each line below the last, so we need to keep track of
    # the culmative height of the lines we've rendered so far
    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = x - fw / 2
        ty = y + y_offset

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh
def wrap_words_to_fit(text, scale, width, x_kerning=0):
    split_on_newlines = text.split("\n")
    if len(split_on_newlines) > 1:
        """if it's got newlines, split it, call this method again, and re-combine"""
        wrapped_substrings = []
        for line in split_on_newlines:
            wrapped_substrings.append(TextImage.wrap_words_to_fit(line, scale, width, x_kerning=x_kerning))

        return "\n".join(wrapped_substrings)

    text = text.replace("\n", " ")  # shouldn't be any at this point, but just to be safe~
    words = text.split(" ")
    lines = []
    cur_line = []

    while len(words) > 0:
        if len(cur_line) == 0:
            cur_line.append(words[0])
            words = words[1:]

        if len(words) == 0:
            lines.append(" ".join(cur_line))
            cur_line.clear()

        elif TextImage.calc_width(" ".join(cur_line + [words[0]]), scale, x_kerning=x_kerning) > width:
            lines.append(" ".join(cur_line))
            cur_line.clear()

        elif len(words) > 0:
            cur_line.append(words[0])
            words = words[1:]
            if len(words) == 0:
                lines.append(" ".join(cur_line))

    return "\n".join(lines)


class OBSOLETE_Textbox(gui.Label):  #use TextArea instead
    """
    """
    def __init__(self,value="",**params):
        super(Textbox,self).__init__(value,**params)
        if('width' in params):
            self.style.width = params['width']

        if('height' in params):
            self.style.height = params['height']

    def resize(self,width=None,height=None):
        return (self.style.width, self.style.height)

    def paint(self,s):
        text.writewrap(s,self.style.font,pygame.Rect(0,0,self.style.width,self.style.height),Const.RED,self.value)


class OBSOLETE_Textlog(gui.Document):
    def __init__(self,**params):
        super(Textlog,self).__init__(**params)
        #self._rect = pygame.Rect(0,0,200,100)
        #self.surface = pygame.Surface(self._rect.size)
        #self.surface.fill(Const.RED)
        self.font = pygame.font.SysFont("sans", 16)
        self.lines = []
        self.set_text("""<div style='border: 1px; border-color: #88ffff; background: #eeffff;' width=700>Welcome to my humble website.</div>""")
        self.set_text("""<p style='border: 1px; border-color: #88ffff; background: #eeffff;' >sdgfs </p>""")
        self.set_text("""<div style='margin: 8px; padding: 8px; border: 1px; border-color: #88ffff; background: #eeffff;' width=700>sdgfs </div>""")

    def __paint(self,s):
        """Renders the label onto the given surface in the upper-left corner."""
        s.blit(self.surface,(0,0))

    def __set_font(self, font):
        """Set the font used to render this label."""
        self.font = font
        # Signal to the application that we need a resize
        self.chsize()

    def __resize(self,width=None,height=None):
        # Calculate the size of the rendered text
        (self.style.width, self.style.height) = self.font.size(self.value)
        #return (self.style.width, self.style.height)
        return self._rect.size

    def set_text(self,text):
        self.lines.append(text)
        _txt="".join(self.lines)
        #self.space((0,0))
        if(len(self.widgets)>0):
            self.remove(self.widgets[0])
        if(len(self.lines)>2):
            self.add(html.HTML(_txt,color=Const.YELLOW,bgcolor=Const.RED))
        #self.add(html.HTML(text,color=Const.YELLOW,bgcolor=Const.RED))
        #self.value=text
        #html.write(self.surface,self.font,self._rect,text,color=Const.YELLOW)
        pass

class OBSOLETE_ListControl(gui.Table):
    """...using a table"""
    def __init__(self,maxRows=5,selectCB=None,**params):
        gui.Table.__init__(self,**params)

        fg = (255,255,255)

        self.tr()
        self.td(gui.Label("My List",color=Const.YELLOW),colspan=2)

        self.tr()
        bt = IconButton("Clickdfsdgffdgdgf 1 Me!")
        #bt.connect(gui.CLICK, resizeMe, bt)
        self.td(bt,align=-1)
        self.tr()
        bt = IconButton("Click  2 Me!")
        self.td(bt,align=-1)
        self.tr()
        bt = IconButton("Click      3 Me!")
        self.td(bt,align=-1)

    def setElements(self,elements):
        """a list of widgets to display"""
        self.allElements = elements
        __updateElements(0)
    
    def __updateElements(page):
         self.clear()
         for i in range(page*self,maxRows,min(len(mylist),(page+1)*self,maxRows)):
            self.tr()
            bt = self.allElements[i]
            self.td(bt,align=-1)