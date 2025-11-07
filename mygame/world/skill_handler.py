# mygame/world/skill_handler.py

# Import all ability classes
from. import abilities 

class SkillHandler:
    """
    Attached to the Character as self.skills.
    Manages learning and executing skills/spells.
    """
    
    # This map REPLACES the giant 'switch' statement in do_cast
    # It maps a string key to the Python class that defines the ability.
    ABILITY_MAP = {
        "fireball": abilities.Fireball,
        "bless": abilities.Bless,
        "poison": abilities.Poison,
        "heal": abilities.Heal,
        "shield of faith": abilities.ShieldOfFaith,
        "bash": abilities.Bash,
        "kick": abilities.Kick,
        "disarm": abilities.Disarm,
        "critical_hit": abilities.CriticalHit,
        "berzerk": abilities.Berzerk,
    }

    def __init__(self, obj):
        self.obj = obj
        if not self.obj.db.known_skills:
            self.obj.db.known_skills = [] # Persistent list of known skills
            
    def initialize(self):
        # Example: give Mages 'fireball' on creation
        if self.obj.class_handler.key == "mage":
             self.learn("fireball")

    def learn(self, skill_key):
        if skill_key in self.ABILITY_MAP and \
           skill_key not in self.obj.db.known_skills:
            self.obj.db.known_skills.append(skill_key)
            self.obj.msg(f"You have learned {skill_key}!")
            
    def execute(self, skill_key, target, **kwargs):
        """
        The main dispatcher. Replaces 'do_cast' logic.
        """
        if skill_key not in self.obj.db.known_skills:
            self.obj.msg("You don't know that ability.")
            return

        ability_class = self.ABILITY_MAP.get(skill_key)
        if not ability_class:
            self.obj.msg("That ability is not implemented.")
            return
            
        # Instantiate the ability class
        ability = ability_class(caster=self.obj)
        
        # 1. Check Rules (mana, cooldowns, etc)
        can_use, reason = ability.check_rules(target, **kwargs)
        if not can_use:
            self.obj.msg(reason)
            return
            
        # 2. Pay Costs
        ability.pay_costs()
        
        # 3. Execute
        ability.at_use(target, **kwargs)