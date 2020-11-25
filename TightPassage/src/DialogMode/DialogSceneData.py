
#you have to pack your dialog into a derived class of this one
class DialogSceneData():
    def __init__(self): 
        pass
    # unique identifier for this scene for example as reference in save file; todo make this a real UID ??
    def GetUId(self):
        return(0)

    #called on starting of display-dialog
    def Setup(self):
        pass

    #gets called from display dialog whenever a button is pressed to switch to the next dialog
    #You have to build a statemachine that returns a dialogtree containing what to display and what choices the player has.
    #The choices have a Choice-ID (unique to this statemachine) and will be fed back by SetDialogResult
    def GetDialog(self):
        return(None)

    #gets called by display dialog when player presses a button. The parameter is the choice-ID connected to the button.  
    def SetDialogResult(self,result):
        pass

class DialogTree(): 
    """ a Dialog tree is a collection of DialogSetups that are chaned together to form a scene
    speakers is a dictionary with Who as key and a tuple specifiying (imagepositon, Font-Color. defaultimage )
    {'Player': (Left, BLUE, 'img01.png'),'Doctor': (Right, RED,'img02.png')}
    """
    def __init__(self,speakers = {'Narrator':{'imageposition':0,'fontcolor':(255,255,255),'defaultimage':None}}):
        self.m_SelectedChoice = 0
        self.m_Set = DialogSetup()
        self.m_Speakers = speakers #{}
    
    def GetSpeakers(self):
        return(self.m_Speakers)

    def GetSetup(self):
        return(self.m_Set)

    def CreateDialogSetup(self):
        self.m_SelectedChoice = 0;
        self.m_Set = DialogSetup()
        #self.m_Set.AddElement(DialogTree.Choice())

    def AddElement(self,Value):
        self.m_Set.AddElement(Value)
    
    def SetDone(self):
        self.m_Set.m_Done = True;
    

    def SetDialogResult(self,choice):
        self.m_SelectedChoice = choice
    
    def GetDialogResult(self):
        return(self.m_SelectedChoice)

    #baseclass for dialog elements
    class DlgElement():
        def __init__(self,position):
            self.m_Position = position

    #a text line
    class Say(DlgElement):
        #Who = ID of the speaker
        #What = Text to Say
        #How = additional Style 
        def __init__(self,Who,What,How=None):
            super().__init__((0,0))
            self.m_Who = Who
            self.m_What = What
            self.m_How = How

    #choice menu
    class Choice(DlgElement):
        def __init__(self,Choices = {'Next':-1}):
            """
            """
            super().__init__((0,0))
            self.m_Choices = Choices   #{}

    #Image
    class Image(DlgElement):
        def __init__(self,position,Who,image):
            super().__init__(position)
            self.m_Who = Who
            self.m_Image = image

#defines a stage setup for dialog (what text to display and how, what images,...)
class DialogSetup():
    def __init__(self): 
        self.m_Elements = [] #new List<DlgElement>();
        self.m_Done = False;
    
    def AddElement(self, Value): 
        self.m_Elements.append(Value)