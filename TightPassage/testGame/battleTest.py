import pygame
from src.GameState import GameState
from src.Components.Party import Character,Party,CharacterReserve
from src.Components.SkillDB import *
from src.BattleMode.BattleController import BattleController,BattleData
from src.BattleMode.BattleScreen import BattleScreenConsole
from src.Interactables.Imp import Imp

def battleTest():

    imp = Imp(pygame.Rect(0,0,0,0))
    imp.draw(None)

    characterReserve=CharacterReserve(character_factory=CharacterReserve.default_character_factory)
    #
    characterReserve.add_char("Heinz")
    char = characterReserve.get_char("Heinz")
    char.addSkill([SkillAttack(),SkillFlee()])
    char.setFaction('Player')
    char.cGraphic = imp.cGraphic
    #
    characterReserve.add_char("Maggy")
    char = characterReserve.get_char("Maggy")
    char.addSkill([SkillAttack(),SkillFlee()])
    char.setFaction('Player')
    char.cGraphic = imp.cGraphic
    #
    characterReserve.add_char("GnollA")
    char = characterReserve.get_char("GnollA")
    char.addSkill([SkillSlashAttack()])
    char.setFaction('Enemy')
    char.cGraphic = imp.cGraphic
    #
    characterReserve.add_char("GnollB")
    char = characterReserve.get_char("GnollB")
    char.addSkill([SkillAttack()])
    char.setFaction('Enemy')
    char.cGraphic = imp.cGraphic

    partyA = Party(characterReserve)
    partyA.initial_state(2)
    partyA.add_char("Heinz")
    partyA.add_char("Maggy")
    partyA.setFaction('Player')

    partyB = Party(characterReserve)
    partyB.initial_state(2)
    partyB.add_char("GnollA")
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