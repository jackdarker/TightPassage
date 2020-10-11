from src.GameState import GameState
from src.Components.Party import Character,Party,CharacterReserve
from src.Components.SkillDB import *
from src.BattleMode.BattleController import BattleController,BattleData
from src.BattleMode.BattleScreen import BattleScreenConsole

def default_character_factory(name):
    char = Character(name)
    return char

game = GameState()
game.reset()

characterReserve=CharacterReserve(character_factory=default_character_factory)
#
characterReserve.add_char("Heinz")
char = characterReserve.get_char("Heinz")
char.addSkill([SkillAttack(),SkillFlee()])
char.setFaction('Player')
#
characterReserve.add_char("Maggy")
char = characterReserve.get_char("Maggy")
char.addSkill([SkillAttack(),SkillFlee()])
char.setFaction('Player')
#
characterReserve.add_char("GnollA")
char = characterReserve.get_char("GnollA")
char.addSkill([SkillSlashAttack()])
char.setFaction('Enemy')
#
characterReserve.add_char("GnollB")
char = characterReserve.get_char("GnollB")
char.addSkill([SkillAttack()])
char.setFaction('Enemy')

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
ctrl = BattleController(game,data)
screen = BattleScreenConsole(None,game,ctrl)
screen.addObserver(ctrl)

Done = False
while(not Done):
    ctrl.update(100)
    screen.update(100)
    Done = ctrl.battleData.battleDone