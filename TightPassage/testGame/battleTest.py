import pygame
import src.Const as Const
import src.Support as Support
from src.GameState import GameState
from src.Components.Party import Character,Party,CharacterReserve
from src.Components.SkillDB import *
from src.BattleMode.BattleController import BattleController,BattleData
from src.BattleMode.BattleScreen import BattleScreenConsole
import src.Components.ResourceManager as RM
from src.Components.ComponentGraphics import ComponentGraphics,AnimData
from src.Interactables.Imp import Imp
from src.Interactables.Player import Player
from src.Vector import Vector2

def battleTest():

    
    def default_character_factory(name):
        char = Character(name,public_data=GameState().StatEngine)   #todo why public statEngine
        return char

    characterReserve=CharacterReserve(character_factory=default_character_factory)
    #
    imp = Player(pygame.Rect(0,0,0,0),0)
    imp.draw(None)
    characterReserve.add_char("Heinz")
    char = characterReserve.get_char("Heinz")
    char.addSkill([SkillAttack(),SkillFlee()])
    char.setFaction('Player')
    char.set_portrait(Const.resource_path("assets/sprites/sample15.png"))
    char.cGraphic = imp.cGraphic
    #
    imp = Player(pygame.Rect(0,0,0,0),0)
    imp.draw(None)
    characterReserve.add_char("Maggy")
    char = characterReserve.get_char("Maggy")
    char.addSkill([SkillAttack(),SkillFlee()])
    char.setFaction('Player')
    char.set_portrait(Const.resource_path("assets/sprites/sample01.png"))
    char.cGraphic = imp.cGraphic
    #

    

    imp = Imp(pygame.Rect(0,0,0,0),direction=Vector2(-1,0))
    imp.draw(None)
    characterReserve.add_char("GnollA")
    char = characterReserve.get_char("GnollA")
    char.addSkill([SkillSlashAttack()])
    char.setFaction('Enemy')
    char.set_portrait(Const.resource_path("assets/sprites/talk.png"))
    cGraphic=ComponentGraphics(char)
    anim = AnimData()
    anim.frames = Support.get_images(RM.get_image("sprites/portrait/destrocrusta01.png"), [[0,0]], (188,210))
    cGraphic.addAnimation("idle",anim)
    cGraphic.switchTo("idle")
    cGraphic.update()
    char.cGraphic = cGraphic
    #
    imp = Imp(pygame.Rect(0,0,0,0),direction=Vector2(-1,0))
    imp.draw(None)
    characterReserve.add_char("GnollB")
    char = characterReserve.get_char("GnollB")
    char.addSkill([SkillAttack()])
    char.setFaction('Enemy')
    char.set_portrait(Const.resource_path("assets/sprites/talk.png"))
    char.cGraphic = imp.cGraphic

    partyA = Party(characterReserve)
    partyA.initial_state(2)
    partyA.add_char("Heinz")
    if(True):
        partyA.add_char("Maggy")
    partyA.setFaction('Player')

    partyB = Party(characterReserve)
    partyB.initial_state(2)
    partyB.add_char("GnollA")
    if(True):
        partyB.add_char("GnollB")
    partyB.setFaction('Enemy')

    data = BattleData()
    data.teams = [partyA,partyB]
    return data


if __name__ == "__main__" :
    pygame.mixer.pre_init(44100, -16, 2, 512) #if this line is not placed before pygame.init there might be delay on sound, also buffersize should be small
    pygame.init()
    screen = pygame.display.set_mode(Const.WINDOW_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF  ) #| pygame.SCALED??
    pygame.mixer.init()
    RM.set_images_path(Const.resource_path("assets"))
    game = GameState()
    game.reset()
    data = battleTest()

    ctrl = BattleController(game,data)
    screen = BattleScreenConsole(game,ctrl)
    screen.addObserver(ctrl)

    Done = False
    while(not Done):
        ctrl.update(100)
        screen.update(100)
        Done = ctrl.battleData.battleDone