import random
import pygame
from src.Components.Skill import Skill,SkillCombat,Effect,SkillResult
import src.Const as Const
from src.Components.Stats import Stats

class EffDamage(Effect):
    def __init__(self,caster,owner,dmg, tick=None):
        super().__init__("Attack",caster,owner,1,tick)
        self.dmg =dmg

    def getDescription(self):
        return ' %s damage ' % (self.dmg)

    def on_apply(self):
        self.owner.damage(self.dmg)
        pass

class EffBleed(Effect):
    def __init__(self,caster,owner,duration,dmg, tick=None):
        super().__init__("Bleeding",caster,owner,duration,tick)
        self.dmg =dmg

    def getDescription(self):
        return ' %s bleeding ' % (self.dmg)

    def on_nextTurn(self):
        super().on_nextTurn()
        if(self.active):
            self.owner.damage(self.dmg)

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
    def __init__(self,name="Attack"):
        super().__init__(name)
        self.filter = self.filterLivingEnemys

    def previewCast(self,targets):
        result = SkillResult()
        result.skill =self
        result.source = self.caster
        result.targets = targets
        if(self.isValidTarget(targets)):
            result.success = True
            for target in targets:
                result.effects.extend(
                    self.calculateDamage(self.caster,target))
        return result

    def calculateDamage(self, caster,target):
        atts = caster.get_stat(Stats.sAttack).value
        atts = atts + random.randint(1, 10) - 5
        defs = target.get_stat(Stats.sDefense).value
        x = atts-defs
        if(x>0):
            return [EffDamage(caster,target,x)]
        else:
            return [EffMiss(caster,target,'missed attack')]
        pass

    def targetFilter(self):
        return self.filter

    def filterLivingEnemys(self,targets):
        return self.targetFilterFighting(
            self.targetFilterEnemy(targets))

class SkillSlashAttack(SkillAttack):
    """execute attack with active weapon that can cause bleed
    """
    def __init__(self):
        super().__init__("Slash")
        pass

    def calculateDamage(self, caster,target):
        atts = caster.get_stat(Stats.sAttack).value
        atts = atts + random.randint(1, 10) - 5
        defs = target.get_stat(Stats.sDefense).value
        x = atts-defs
        if(x>0):
            return [EffDamage(caster,target,x),EffBleed(caster,target,2,x)]
        else:
            return [EffMiss(caster,target,'missed attack')]
        pass

class SkillSmokeBomb(SkillAttack):
    """execute attack with active weapon that can cause bleed
    """
    def __init__(self):
        super().__init__("Slash")
        pass

    def calculateDamage(self, caster,target):
        atts = caster.get_stat(Stats.sAttack).value
        atts = atts + random.randint(1, 10) - 5
        defs = target.get_stat(Stats.sDefense).value
        x = atts-defs
        if(x>0):
            return [EffDamage(caster,target,x),EffBleed(caster,target,2,x)]
        else:
            return [EffMiss(caster,target,'missed attack')]
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