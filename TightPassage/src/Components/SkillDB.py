import random
import pygame
from src.Components.Skill import Skill,SkillCombat,Effect,SkillResult
import src.Const as Const

class EffDamage(Effect):
    def __init__(self,caster,owner,dmg, tick=None):
        super().__init__("Attack",caster,owner,1,tick)
        self.dmg =dmg

    def getDescription(self):
        return ' %s damage ' % (self.dmg)

    def on_apply(self):
        self.owner.damage(self.dmg)
        self.remove()
        pass

class EffMiss(Effect):
    """placeholder effect if the calculation indicates that the skill misses
    """
    def __init__(self,caster,owner,descr, tick=None):
        super().__init__("Missed",caster,owner,1,tick)
        self.descr=descr

    def getDescription(self):
        return self.descr

    def on_apply(self):
        self.remove()
        pass

class EffFlee(Effect):
    def __init__(self,caster,owner, tick=None):
        super().__init__("Flee",caster,owner,2,tick)


##########################################################
class SkillAttack(SkillCombat):
    """execute simple attack with active weapon
    """
    def __init__(self):
        super().__init__("Attack")
        pass

    def previewCast(self,targets):
        result = SkillResult()
        
        if(self.isValidTarget(targets)):
            result.success = True
            for target in targets:
                result.effects.append(self.calculateDamage(self.caster,target))
        return result

    def calculateDamage(self, caster,target):
        atts = caster.stats.Att
        atts = atts + random.randint(1, 10) - 5
        defs = target.stats.Def
        x = atts-defs
        if(x>0):
            return EffDamage(caster,target,x)
        else:
            return EffMiss(caster,target,'missed attack')
        pass

class SkillFlee(SkillCombat):
    """try to retreat from combat
    """
    def __init__(self):
        super().__init__("Flee")
        pass

    def targetFilter(self):
        return self.targetFilterSelf

    def previewCast(self,targets):
        result = SkillResult()
        
        if(self.isValidTarget(targets)):
            result.success = True
            for target in targets:
                result.effects.append(EffFlee(self.caster,target))
        return result

class SkillDB():
    def __init__(self):
        pass