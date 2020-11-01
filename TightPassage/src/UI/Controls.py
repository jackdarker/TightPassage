import pygame
import time
import random
from pygame.locals import *
import src.Const as Const
from src.UI.pgu.pgu import gui
from src.UI.pgu.pgu import html


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
        #when the toolbutton is pressed it will call gui.CHANGE->tab() and this will switchout the boxwidget with c,t or d
        noPages= 0
        pageSize = (0,0)
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

    #function called when clicking tablabels to switch tab
    def _switchTab(self):
        self.box.widget = self.tabs.value

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

        textWidth=scrollWidth=0
        if('width' in params):
            textWidth = params['width']-100
            scrollWidth = params['width']-50

        self.maxScrollHeight =0
        self.minScrollHeight = 30
        if('height' in params):
            self.maxScrollHeight = params['height']
        self.layout = gui.Table()

        
        self.doc = gui.Document(width=textWidth)
        self.scrollList = gui.ScrollArea(self.doc,width=scrollWidth,height=self.maxScrollHeight,hscrollbar=False, vscrollbar=True)
        
        self.font = pygame.font.SysFont("sans", 16)     #todo styling
        self.doc.block(align=-1)

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
        

    def set_text(self,text):
        space = self.font.size(" ")
        for word in text.split(" "): 
            self.doc.add(gui.Label(word))
            self.doc.space(space)
        self.doc.br(space[1])
        self.scrollList.set_vertical_scroll(65535)  #scrolls automat. to end of list

    def clear_text(self):
        self.doc.remove_all()
        #add at least space or area shrinks to 0
        space = self.font.size(" ")
        self.doc.br(space[1])

    def toggle_expand(self):
        if(self.is_expanded):
            self.style.height=self.doc.style.height=self.scrollList.style.height= self.minScrollHeight
        else:
            self.style.height=self.doc.style.height=self.scrollList.style.height= self.maxScrollHeight
        self.is_expanded = not self.is_expanded
        self.scrollList.chsize()
        self.doc.chsize() 
        self.chsize()
        self.set_text('Cuzcos Paint is a revolutionary new paint program it has all the awesome features that you need to paint really great pictures.')


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

#OBSOLETE !
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