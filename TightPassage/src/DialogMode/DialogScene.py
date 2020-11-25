import pygame
import pygame_menu
import src.Const as Const
import src.GameMode as GameMode
import src.Components.ResourceManager as RM
from src.UI.Controls import *
from src.UI.pgu.pgu import gui
from src.DialogMode.DialogSceneData import *
from src.Components.ComponentGraphics import ComponentGraphics,AnimData

""" renders a dialog by cycling through DialogSceneData
"""
class DialogScene(GameMode.GameMode):
    """
    possible params:
        minImgageWidth = 200      #specify the space to reserve for each image; 0 might disable them

    windowLayout 1:
        -----------------------------------------
        | img   | text                  | img   |
        | left  | text                  | right |
        |       | text                  |       |
        |       |-----------------------|       |
        |       | choice 1 / next       |       |
        |       | choice 2              |       |
        |       | choice 3              |       |
        |       | choice 4              |       |
        -----------------------------------------

    windowLayout 2:
        ----------------------------------------
        |        img                           |
        |        center                        |
        |                                      |
        |                                      |
        |--------------------------------------|
        | text                                 |
        | choice 1  choice 2                   |
        ----------------------------------------

    """

    def __init__(self,state,on_done=None,**params):
        params.setdefault('minImgageWidth',200)
        params.setdefault('windowLayout',2)
        self.windowLayout = params.get("windowLayout", 1)
        super().__init__(state)
        self.rect = pygame.Rect((0,0),Const.WINDOW_SIZE)
        self.cGraphic = ComponentGraphics(self)
        self.enabled=False
        self.scene = None
        self.on_done = on_done
        #self.spriteGroup = pygame.sprite.Group() #holder for all battler-sprites
        self.bg = pygame.Surface(Const.WINDOW_SIZE)
        self.bg.fill((100,100,100,100))
        self._setupHud()

    def _setupHud(self):
        self.form = gui.Form()
        themetouse = Const.resource_path("assets/pgu_themes/game") #("default")
        self.app = gui.App(theme=gui.Theme(themetouse))
        #the container for the widgets
        c = gui.Container(align=0,valign=0)
        
        #layout container
        layoutCtrl = gui.Table(align=0,valign=0) #centered on screen; 
        #calculation of sizes depends on rect-size
        margintop = 10
        marginleft = 10

        if(self.windowLayout==2):
            textheight = 100
            tabsheetHeight =200
            imageheight = self.rect.height-textheight -tabsheetHeight - margintop *2

            if(self.rect.width>600):
                marginleft = 30
                imagewidth = self.rect.width*2//3
            else:
                imagewidth = self.rect.width-marginleft*2
            textwidth = imagewidth

        else:
            if(self.rect.height>600):
                margintop = 30
                textheight = self.rect.height*2//3
            else:
                textheight = self.rect.height-150
            tabsheetHeight = self.rect.height-textheight - 2* margintop

            if(self.rect.width>600):
                marginleft = 30
                textwidth = self.rect.width*2//3
            else:
                textwidth = self.rect.width-200
            imagewidth = (self.rect.width - textwidth- 2* marginleft)//2


        #self.Log = gui.TextArea(value="",focusable=False,editable=False,width=textwidth-6, height=textheight-6)
        self.Log = html.HTML("""</p>""",width=textwidth-6, height=textheight-6)
        self.Scroll = gui.ScrollArea(self.Log,hscrollbar=False, vscrollbar=True, width=textwidth, height=textheight)
        if(self.windowLayout==2):
            btColumn = 0
            self.ImageLeft = gui.Image(Const.resource_path("assets\\sprites\\portrait\\monster04.png"),width=imagewidth, height = imageheight,scaleSymetric = False)
            layoutCtrl.tr()
            layoutCtrl.td(self.ImageLeft,height = imageheight)
            layoutCtrl.tr()
            layoutCtrl.td(self.Scroll)
        else:
            btColumn=1
            self.ImageLeft = gui.Image(pygame.Surface((0,0)))
            self.ImageRight = gui.Image(Const.resource_path("assets\\sprites\\sample15.png"))
            layoutCtrl.tr()
            layoutCtrl.td(self.ImageLeft,width=imagewidth)
            layoutCtrl.td(self.Scroll)
            layoutCtrl.td(self.ImageRight,width=imagewidth)

        #grid with buttons
        self.tbButtons = gui.Table(align=0,valign=-1)
        self.tbButtons.style.width = textwidth
        self.tbButtons.style.height = tabsheetHeight
        layoutCtrl.tr()
        layoutCtrl.add(self.tbButtons,col=btColumn)

        c.add(layoutCtrl,0,0)
        self.app.init(c)
        pass

    def startScene(self, scene):
        self.scene = scene
        self.scene.Setup()
        self._next()
        self.show()
    
    def _next(self):
        dlg = self.scene.GetDialog().GetSetup()
        if(dlg.m_Done==True):
            self._on_done()
            return
        speakers = self.scene.GetDialog().GetSpeakers()
        imageLeft = imageRight = None
        for element in dlg.m_Elements:
            if(type(element) == DialogTree.Say):
                if(speakers[element.m_Who]['imageposition'] == 1):
                    if(imageRight == None):
                        imageRight = speakers[element.m_Who]['defaultimage']
                else:
                    if(imageLeft == None):
                        imageLeft = speakers[element.m_Who]['defaultimage']
                self.Log.set_html( element.m_What) #.value = element.m_What

            elif(type(element) == DialogTree.Image):
                if(speakers[element.m_Who]['imageposition'] == 1):
                    imageRight = element.m_Image
                else:
                    imageLeft = element.m_Image
            elif(type(element) == DialogTree.Choice):
                self._createButtons(self.tbButtons,element.m_Choices,self._choice)

        if(self.windowLayout==1):  #todo this looks shitty
            if(imageLeft != None):
                self.ImageLeft.set_image(imageLeft)
            if(imageRight != None):
                self.ImageRight.set_image(imageRight)
        else:
            if(imageLeft != None):
                self.ImageLeft.set_image(imageLeft)
            if(imageRight != None):
                self.ImageLeft.set_image(imageRight)

    def _choice(self, value):
        self.scene.SetDialogResult(value)
        self._next()

    def _on_done(self):
        if(self.on_done!=None):
            self.on_done()

    def _createButtons(self,btTable,choices, clickCallback):
        """creates a button grid. 
            choices is dictionary of strings with int
            callback is a function which will receive the object from the list
        """
        #todo if list to big, create multiple pages
        for bt in btTable.widgets:
            bt.disconnect(gui.CLICK)
        btTable.clear()

        lstItems = []
        if(type(choices)==dict):
            lstItems = list(choices)

        size = len(lstItems)
        i=0
        #for y in range(0,5):    #todo fill up cols first, not rows
        #    btTable.tr()
        for x in range(0,3):
            for y in range(0,5):
                if(size>i):
                    if(type(lstItems[i])==str):
                        label=lstItems[i]
                    else:
                        label=lstItems[i].name
                    bt = IconButton(label)
                    bt.disabled=False
                    bt.connect(gui.CLICK, clickCallback, choices[lstItems[i]])
                    btTable.td(bt,align=0,valign=0,col=x,row=y)
                #else:
                    #bt = IconButton("---")
                    #bt.disabled=True
                    #btTable.td(bt,align=-1)
                i+=1
        btTable.resize() #todo why do I get issues when not resizing here
    
    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE \
                or event.key == pygame.K_SPACE \
                or event.key == pygame.K_RETURN:
                    self.notifyShowMenuRequested()
                    self.enabled = False
            else:
                self.app.event(event)
                    
    def update(self,dt):
        #self.spriteGroup.update(dt)

        pass

    def render(self, window):
        window.blit(self.bg,(0,0))
        #self.spriteGroup.draw(window)
        self.app.paint(window) #pgu gui update

    def show(self):
        self.enabled = True