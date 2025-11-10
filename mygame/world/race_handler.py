# mygame/world/race_handler.py

# Import all race definitions
from . import races

class RaceHandler:
    """
    Attached to the Character as self.race_handler.
    Manages all race-specific logic.
    """

    RACE_MAP = {
        "human": races.Human,
        "aarakocra": races.Aarakocra,
        "alaghi": races.Alaghi,
        "archon": races.Archon,
        "avatar": races.Avatar,
        "barbarian": races.Barbarian,
        "bugbear": races.Bugbear,
        "bullywug": races.Bullywug,
        "centaur": races.Centaur,
        "changeling": races.Changeling,
        "daemon": races.Daemon,
        "demi-god": races.DemiGod,
        "draconian": races.Draconian,
        "drow": races.Drow,
        "dwarf": races.Dwarf,
        "eldar": races.Eldar,
        "elemental": races.Elemental,
        "elf": races.Elf,
        "fairy": races.Fairy,
        "flind": races.Flind,
        "giant": races.Giant,
        "giff": races.Giff,
        "githzerai": races.Githzerai,
        "gnoll": races.Gnoll,
        "gnome": races.Gnome,
        "golem": races.Golem,
        "half-elf": races.HalfElf,
        "half-ogre": races.HalfOgre,
        "half-orc": races.HalfOrc,
        "halfling": races.Halfling,
        "lich": races.Lich,
        "lizardman": races.Lizardman,
        "minotaur": races.Minotaur,
        "prophet": races.Prophet,
        "ratman": races.Ratman,
    }

    def __init__(self, obj):
        self.obj = obj
        # Set persistent defaults
        if not self.obj.db.race_key:
            self.obj.db.race_key = "human" # Default

    def initialize(self):
        """Called at creation."""
        pass

    def get_race_obj(self):
        """Returns an *instance* of the character's current race."""
        race_definition = self.RACE_MAP.get(self.obj.db.race_key)
        return race_definition() # Instantiate and return
