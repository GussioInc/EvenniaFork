# mygame/world/class_handler.py

import random
# Import all class definitions
from. import classes 

class ClassHandler:
    """
    Attached to the Character as self.class_handler.
    Manages level, XP, and all class-specific logic.
    """
    
    # This map REPLACES class.c tables
    CLASS_MAP = {
        "rogue": classes.Rogue,
        "paladin": classes.Paladin,
        "monk": classes.Monk,
        "druid": classes.Druid,
        "bard": classes.Bard,
        "assassin": classes.Assassin,
        "darkknight": classes.DarkKnight,
        "ranger": classes.Ranger,
        "priest": classes.Priest,
        "swordsman": classes.Swordsman,
        "wizard": classes.Wizard,
        "necromancer": classes.Necromancer,
        "pirate": classes.Pirate,
    }
    
    def __init__(self, obj):
        self.obj = obj
        # Set persistent defaults
        if not self.obj.db.level:
            self.obj.db.level = 1
        if not self.obj.db.xp:
            self.obj.db.xp = 0
        if not self.obj.db.class_key:
            self.obj.db.class_key = "swordsman" # Default
            
    def initialize(self):
        """Called at creation."""
        pass

    def get_class_obj(self):
        """Returns an *instance* of the character's current class."""
        class_definition = self.CLASS_MAP.get(self.obj.db.class_key)
        if not class_definition:
            # Fallback to a default if the saved class key is invalid
            class_definition = self.CLASS_MAP.get("swordsman")
        return class_definition() # Instantiate and return

    @property
    def level(self):
        return self.obj.db.level
        
    @property
    def xp(self):
        return self.obj.db.xp

    def check_for_level_up(self):
        """
        Called by Character.gain_exp.
        Checks for new skills to learn.
        """
        class_obj = self.get_class_obj()
        level = self.obj.db.level
        
        # In the new system, skills are not learned by level.
        # This can be expanded later.
        pass
            
    def do_level_up(self, class_obj):
        """Performs all logic for gaining a level."""
        # This method is not currently used, but is kept for future expansion.
        pass