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
        **{ability.key: ability for ability in abilities.BaseAbility.__subclasses__()},
    }

    def __init__(self, obj):
        self.obj = obj
        if not self.obj.db.known_skills:
            self.obj.db.known_skills = {} # {skill_key: {"proficiency": 1, "max": 100}}
            
    def initialize(self):
        # We will learn skills via the class handler now
        pass

    def learn(self, skill_key, max_proficiency=100):
        if skill_key in self.ABILITY_MAP and \
           skill_key not in self.obj.db.known_skills:
            self.obj.db.known_skills[skill_key] = {"proficiency": 1, "max": max_proficiency}
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