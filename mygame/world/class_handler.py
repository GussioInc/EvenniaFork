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
        "warrior": classes.Warrior,
        "mage": classes.Mage,
    }
    
    def __init__(self, obj):
        self.obj = obj
        # Set persistent defaults
        if not self.obj.db.level:
            self.obj.db.level = 1
        if not self.obj.db.xp:
            self.obj.db.xp = 0
        if not self.obj.db.class_key:
            self.obj.db.class_key = "warrior" # Default
            
    def initialize(self):
        """Called at creation."""
        # Get the class object and set initial HP/MP
        class_obj = self.get_class_obj()
        self.obj.vitals.HP.base = class_obj.base_hp
        self.obj.vitals.MP.base = class_obj.base_mp
        self.obj.vitals.HP.current = class_obj.base_hp
        self.obj.vitals.MP.current = class_obj.base_mp

    def get_class_obj(self):
        """Returns an *instance* of the character's current class."""
        class_definition = self.CLASS_MAP.get(self.obj.db.class_key)
        return class_definition() # Instantiate and return

    @property
    def level(self):
        return self.obj.db.level
        
    @property
    def xp(self):
        return self.obj.db.xp

    # (Properties for base_hp, hp_per_level, etc. are defined
    # on the class_obj, which we access in Character.max_hp)

    def check_for_level_up(self):
        """
        Called by Character.gain_exp.
        Checks XP against the class-specific XP table.
        """
        class_obj = self.get_class_obj()
        current_level = self.obj.db.level
        
        xp_needed = class_obj.xp_table.get(current_level + 1)
        if not xp_needed:
            return # Max level
            
        if self.obj.db.xp >= xp_needed:
            self.do_level_up(class_obj)
            
    def do_level_up(self, class_obj):
        """Performs all logic for gaining a level."""
        self.obj.db.level += 1
        level = self.obj.db.level
        
        self.obj.msg(f"|gYou have advanced to Level {level}!|n")
        
        # 1. Roll for and add HP/MP
        con_mod = (self.obj.stats.CON.value - 10) // 2
        int_mod = (self.obj.stats.INT.value - 10) // 2
        
        hp_gain = random.randint(1, class_obj.hit_die) + con_mod
        mp_gain = random.randint(1, class_obj.mana_die) + int_mod
        
        # Delegate to VitalsHandler
        self.obj.vitals.at_new_level(hp_gain, mp_gain)
        self.obj.msg(f"You gain {hp_gain} HP and {mp_gain} MP.")
        
        # 2. Add new skills
        new_skills = class_obj.skills_at_level.get(level,)
        for skill_key in new_skills:
            self.obj.skills.learn(skill_key) # Delegate to SkillHandler
            
        # 3. Check for another level-up (for multi-level gains)
        self.check_for_level_up()