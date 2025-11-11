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
        "elf": races.Elf,
        "half-elf": races.HalfElf,
        "dwarf": races.Dwarf,
        "gnome": races.Gnome,
        "halfling": races.Halfling,
        "barbarian": races.Barbarian,
        "half-orc": races.HalfOrc,
        "half-ogre": races.HalfOgre,
        "changeling": races.Changeling,
        "fairy": races.Fairy,
        "minotaur": races.Minotaur,
        "ratman": races.Ratman,
        "drow": races.Drow,
        "lizardman": races.Lizardman,
        "giant": races.Giant,
        "draconian": races.Draconian,
        "centaur": races.Centaur,
        "aarakocra": races.Aarakocra,
        "alaghi": races.Alaghi,
        "bugbear": races.Bugbear,
        "bullywug": races.Bullywug,
        "flind": races.Flind,
        "giff": races.Giff,
        "githzerai": races.Githzerai,
        "gnoll": races.Gnoll,
        "wemic": races.Wemic,
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
