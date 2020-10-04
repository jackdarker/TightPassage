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
characterReserve.add_char("Heinz")
characterReserve.get_char("Heinz").skills = [SkillAttack()]
characterReserve.add_char("Gnoll")

partyA = Party(characterReserve)
partyA.initial_state(2)
partyA.add_char("Heinz")

partyB = Party(characterReserve)
partyB.initial_state(2)
partyB.add_char("Gnoll")

data = BattleData()
data.teams = [partyA,partyB]
ctrl = BattleController(game,data)
screen = BattleScreenConsole(None,game,ctrl)
screen.addObserver(ctrl)

Done = False
while(not Done):
    ctrl.update(100)
    screen.update(100)