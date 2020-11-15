#class TargetFilter():
#    def __init__(self,name):
#        pass
#    def targetFilter(self,targets):
#        return []

class Skill():
    """an action the character can do
    """
    def __init__(self,name):
        self.name = name
        self.caster = None
        pass

    @property
    def caster(self):
        """the character that is casting"""
        return self._caster

    @caster.setter
    def caster(self,caster):
        self._caster = caster


    def getMaxTargetCount(self):
        return 1

    def targetFilter(self):
        """returns a function to filter a list of possible targets for targets that this skill can cast on
        myFilter(targets)->targets   teams is a array of party; targets is a list of character
        """
        return self.targetFilterEnemy

    def isValidPhase(self):
        """returns True if the skill can be used in tha actual game-phase (combatPhase,explorePhase)
        """
        return True

    def isDisabled(self):
        """returns True and text if the skill cannot be used because its temporary disabled (silenced mage, blinded)
        the text should indicate why and how long it is disabled
        """
        return False,''

    def isValidTarget(self,targets):
        """returns True if the skill can be used on the target(s)"""
        return (sorted(self.targetFilter()(targets))== sorted(targets))

    def getCost(self):
        """returns information about the cost to execute the skill"""
        return {}

    def getName(self):
        """returns name of the skill for listboxes/labels"""
        return self.name

    def getDescription(self):
        """returns a description of the skill for tooltip"""
        return self.name

    def getRenderData(self):
        """
        """
        return None


    def previewCast(self,targets):
        result = SkillResult()
        return result

    def cast(self,targets):
        """execute the skill on the targets"""
        pass

    #some predefined filter; chain them to narrow down the targets
    def targetFilterSelf(self,targets):
        possibleTarget = []
        for target in targets:
            if(self.caster.name == target.name):
                possibleTarget.append(target)
        return possibleTarget

    def targetFilterAlly(self,targets):
        possibleTarget = []
        for target in targets:
            if(self.caster.faction == target.faction):
                possibleTarget.append(target)
        return possibleTarget

    def targetFilterEnemy(self,targets):
        possibleTarget = []
        for target in targets:
            if(self.caster.faction != target.faction):
                possibleTarget.append(target)
        return possibleTarget

    def targetFilterFighting(self,targets):
        """chars that are not inhibited"""
        possibleTarget = []
        for target in targets:
            if(not target.isInhibited()):
                possibleTarget.append(target)
        return possibleTarget

    def targetFilterDead(self,targets):
        """chars that are dead"""
        possibleTarget = []
        for target in targets:
            if(not target.isDead()):
                possibleTarget.append(target)
        return possibleTarget

class SkillCombat(Skill):
    """a skill that can only be used in combat"""
    def isValidPhase(self):
        """returns True if the skill can be used in tha actual game-phase (combatPhase,explorePhase)
        """
        return True #todo

    def targetFilter(self):
        """returns a function to filter a list of possible targets for targets that this skill can cast on
        myFilter(targets)->targets   teams is a array of party; targets is a list of character
        """
        return self.targetFilterEnemy

class Effect():
    """ Effects are actions that trigger after a certain action is made
    'name' is the identifier used to identify the effect
    duration is used to indicate how long the effect will last on the
    target. Durations for each effect on a target are decreased by 1
    after that character's turn
    """
    def __init__(self,name,caster,owner, duration, tick=None):
        self.name = name
        self.max_duration = duration
        self.duration = duration 
        self.tick = tick 
        if not tick:
            self.cur_tick = 0
        else:
            self.cur_tick = self.max_duration - tick
        self.active = True
        self.owner = owner
        self.caster = caster

    @property
    def owner(self):
        """the character that is casting"""
        return self._owner

    @owner.setter
    def owner(self,owner):
        self._owner = owner

    @property
    def caster(self):
        """the character that is casting"""
        return self._caster

    @caster.setter
    def caster(self,caster):
        self._caster = caster

    def getDescription(self):
        """returns a description of the effect for view"""
        return self.__str__()

    def remove(self):
        """Inactivates and removes effect
        When called any subsequent calls to this effect will be ignored as
        well as removed useful for 1 time effects
        """
        self.duration = 0
        self.active = False

    def on_apply(self):
        """called to add the effect to the character"""
        self.owner.effects.append(self)  #todo some effects should not append multiple times?
        pass

    def on_remove(self):
        if(self in self.owner.effects):
            self.owner.effects.remove(self)
        pass

    def on_nextTurn(self):
        self.duration-=1
        if(duration<=0 and self.active):
            self.on_remove()
        pass

    def on_combatEnd(self):
        pass

    def on_combatStart(self):
        pass

    def __str__(self):
        if(self.max_duration<=1):
            return "%s " % (self.name.replace("-", " ").title())
        else:
            return "%s - Turn(s) %s" % (self.name.replace("-", " ").title(),self.duration)

class SkillResult():
    def __init__(self):
        self.success = False
        self.source = None
        self.targets = []
        self.skill = None
        self.effects = []
        pass

