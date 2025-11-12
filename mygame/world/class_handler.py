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
        "warrior/thief": classes.WarriorThief,
        "warrior/cleric": classes.WarriorCleric,
        "warrior/magic-user": classes.WarriorMagicUser,
        "thief/cleric": classes.ThiefCleric,
        "thief/magic-user": classes.ThiefMagicUser,
        "cleric/magic-user": classes.ClericMagicUser,
        "warrior/thief/cleric": classes.WarriorThiefCleric,
        "warrior/thief/magic-user": classes.WarriorThiefMagicUser,
        "warrior/cleric/magic-user": classes.WarriorClericMagicUser,
        "thief/cleric/magic-user": classes.ThiefClericMagicUser,
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
        Checks XP against the class-specific XP table.
        """
        class_obj = self.get_class_obj()
        current_level = self.obj.db.level
        
        # XP-based leveling is disabled until xp_tables are added to classes
        # xp_needed = class_obj.xp_table.get(current_level + 1)
        # if not xp_needed:
        #     return # Max level
        #
        # xp_needed *= class_obj.num_classes
        #
        # if self.obj.db.xp >= xp_needed:
        #     self.do_level_up(class_obj)

        # For now, just learn skills based on current level
        for skill_key, max_prof in class_obj.skills.items():
             self.obj.skills.learn(skill_key, max_proficiency=max_prof)
            
    def do_level_up(self, class_obj):
        """Performs all logic for gaining a level."""
        self.obj.db.level += 1
        level = self.obj.db.level

        self.obj.msg(f"|gYou have advanced to Level {level}!|n")

        # HP/MP gains can be added back here when hit_die/mana_die are on classes

        # 3. Check for another level-up (for multi-level gains)
        self.check_for_level_up()