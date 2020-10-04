import pygame
from src.Components.Skill import Skill,SkillCombat,Effect
import src.Const as Const

class EffDamage(Effect):
    def __init__(self,caster,owner, tick=None):
        super().__init__("Attack",caster,owner,1,tick)

    def on_apply(self):
        self.owner.damage(10)
        self.remove()
        pass

class EffFlee(Effect):
    def __init__(self,caster,owner, tick=None):
        super().__init__("Flee",caster,owner,1,tick)

    def on_nextTurn(self):
        #todo GameState().retreatFromCombat()
        pass
##########################################################
class SkillAttack(SkillCombat):
    """execute simple attack with active weapon
    """
    def __init__(self):
        super().__init__("Attack")
        pass

    def cast(self,targets):
        if(self.isValidTarget(targets)):
            for target in targets:
                target.addEffect(EffDamage())
        pass

class SkillFlee(SkillCombat):
    """try to retreat from combat
    """
    def __init__(self):
        super().__init__("Flee")
        pass

    def targetFilter(self):
        """returns a function to filter a list of possible targets for targets that this skill can cast on
        myFilter(targets)->targets
        """
        return Skill.targetFilterAlly

    def cast(self,targets):
        if(self.isValidTarget(targets)):
            for target in targets:
                target.addEffect(EffDamage())
                break
        pass