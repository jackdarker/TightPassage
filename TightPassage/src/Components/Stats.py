from src.Components.StatEngine import *

class Stats():
    #core stats
    sDexterity = "Dexterity"
    sIntelligence = "Intelligence"
    sStrength = "Strength"
    sWisdom = "Wisdom"
    sCharisma = "Charisma"
    sConstitution = "Constitution"
    CORE_STAT_NAMES = (sDexterity,sIntelligence,sStrength,sWisdom,sCharisma,sConstitution)
    CORE_STAT_STANDARD_ARRAY = (10, 9, 11, 8, 10, 8)

    sSkills = "Skills"
    sAttributes = "Attributes"


    def __init__(self):
        self.maxHP = 10
        self.HP = 10
        self.Att = 3
        self.Def = 2
        pass

class MaxHP(RPGDerivedStat):
    def __init__(self, owner ):
        super(MaxHP,self).__init__(__class__.__name__, Stats.sAttributes, owner)
        self.add_dependency(Stats.sConstitution)

    def calculate(self):
        con = self.get_dependency_value(Stats.sConstitution)
        return 10 + con
    pass

class HP(RPGDerivedStat):
    def __init__(self, owner ):
        super(HP,self).__init__(__class__.__name__, Stats.sAttributes, owner)
        self.add_dependency(MaxHP.__name__)
        self.add_dependency("Damage",optional=True,default_value=0)

    def calculate(self):
        max_HP = self.get_dependency_value(MaxHP.__name__)
        dmg = self.get_dependency_value("Damage")
        if dmg < 0:
            dmg = 0
        return max_HP - dmg

# A Lock-picking Skill stat based on Dex and Int
class Lockpicking(RPGDerivedStat):

    def __init__(self, owner ):#: RPGObject):
        super(Lockpicking,self).__init__(__class__.__name__, Stats.sSkills, owner)
        self.add_dependency(Stats.sDexterity)
        self.add_dependency(Stats.sIntelligence)

    def calculate(self):
        dex = self.get_dependency_value(Stats.sDexterity)
        intell = self.get_dependency_value(Stats.sIntelligence)
        return dex + intell