
def targetFilterAlly(targets):
    possibleTarget = []
    for target in targets:
        if(target.isPlayerAlly()):
            possibleTarget.append(target)

def targetFilterEnemy(targets):
    possibleTarget = []
    for target in targets:
        if(not target.isPlayerAlly()):
            possibleTarget.append(target)

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
        myFilter(targets)->targets
        """
        return targetFilterEnemy

    def isValidPhase(self):
        """returns True if the skill can be used in tha actual game-phase (combatPhase,explorePhase)
        """
        return True

    def isValidTarget(self,targets):
        """returns True if the skill can be used on the target(s)"""
        return (self.targetFilter(targets).sorted()== targets.sorted())

    def getCost(self):
        """returns infomration about the cost to execute the skill"""
        return {}

    def getDescription(self):
        """returns a description of the skill for view"""
        return self.name

    def cast(self,targets):
        """execute the skill on the targets"""
        pass

class SkillCombat(Skill):
    """a skill that can only be used in combat"""
    def isValidPhase(self):
        """returns True if the skill can be used in tha actual game-phase (combatPhase,explorePhase)
        """
        return True #todo

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
        pass

    def on_remove(self):
        pass

    def on_nextTurn(self):
        pass

    def on_combatEnd(self):
        pass

    def on_combatStart(self):
        pass

    def __str__(self):
        return "%s - Turn(s) %s" % (self.name.replace("-", " ").title(),
                                   self.duration)