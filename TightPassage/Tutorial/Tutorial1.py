import src.Const as Const
from src.DialogMode.DialogSceneData import *
from src.Data.Quest.QuestGlobals import Scene_Enum, NPC_Enum

class Tutorial1(DialogSceneData):

    def __init__(self):
        super().__init__()
        self.m_State = 0
        speakers = {NPC_Enum.Narrator: {'imageposition':1,'fontcolor':(255,0,0),'defaultimage':Const.resource_path("assets\\sprites\\portrait\\monster04.png")} ,
                    NPC_Enum.Player:   {'imageposition':0,'fontcolor':(255,255,255),'defaultimage':Const.resource_path("assets\\sprites\\sample01.png")}} 
        self.dlg = DialogTree(speakers)
        


    def GetUId(self):
        return(Scene_Enum.Tutorial1)

    def Setup(self):
        self.m_State = 0

    def SetDialogResult(self,result):
        self.dlg.SetDialogResult(result);
        pass

    def GetDialog(self):
        _choice = self.dlg.GetDialogResult();
        if (_choice > 0): self.m_State = _choice;
        elif(_choice == -1):    #Next -> step forward
            self.m_State +=1
        #if (m_State == 0):
        #    QuestGlobals.getSingleton();    //Todo rebuild quest on Start/load
        #    int _GoogleQuestMile = QuestManager.getSingleton().GetQuestById((int)QuestGlobals.QuestEnum.QstWiseManGoogles).GetCurrMile().GetUId();
        #    if (_GoogleQuestMile >= (int)QstWiseManGoogles.MileEnum.HuntGoogleQuest1 && _GoogleQuestMile < (int)QstWiseManGoogles.MileEnum.HuntGoogleQuest2):
        #        m_State = 10;
        self._dialog(self.m_State)
        return(self.dlg)

    def _dialog(self,state):
        self.dlg.CreateDialogSetup();
        _Say = DialogTree.Say("Narrator","");
        _Say.m_Who = NPC_Enum.Narrator;
        _Choice= DialogTree.Choice( ) #choice=Next

        if(state == 1):
            _Say.m_Who = NPC_Enum.Player;
            _Say.m_What = "I have some questions";
            _Choice= DialogTree.Choice( {"Who are you?":2, "No":3 })
        elif(state == 2):
            _Say.m_What = "Im the guy how explains everything to you. ...Sigh.";
        elif(state == 3):
            _Say.m_Who = NPC_Enum.Player;
            _Say.m_What = "ok.";
        elif(state == 4):
            self.dlg.SetDone()
        else: #state == 0
            _Say.m_What = """<div style='color:red;'>this is normal <b>this is bold</b> <i>this is italic</i> <u>this is underline</u>
            Turnbased battle mode \n To fight an enemy, select a skill and a target. \n The fight ends when everyone from a team has no health left.</div>""";

        self.dlg.AddElement(_Say);
        self.dlg.AddElement(_Choice);
        pass