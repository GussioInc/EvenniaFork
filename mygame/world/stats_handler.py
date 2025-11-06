# mygame/world/stats_handler.py
from evennia.contrib.rpg.traits import TraitHandler

class StatsHandler(TraitHandler):
    """
    Manages the 6 core D&D stats using Static Traits.
    """
    def __init__(self, obj):
        """Uses a different attribute key to stay separate from vitals."""
        super().__init__(obj, db_attribute_key="stats")
        
    def initialize(self):
        """Called by Character.at_object_creation to set defaults."""
        self.add("STR", "Strength", trait_type="static", base=10)
        self.add("DEX", "Dexterity", trait_type="static", base=10)
        self.add("CON", "Constitution", trait_type="static", base=10)
        self.add("INT", "Intelligence", trait_type="static", base=10)
        self.add("WIS", "Wisdom", trait_type="static", base=10)
        self.add("CHA", "Charisma", trait_type="static", base=10)

# mygame/world/vitals_handler.py
from evennia.contrib.rpg.traits import TraitHandler

class VitalsHandler(TraitHandler):
    """
    Manages dynamic gauges like HP and Mana.
    """
    def __init__(self, obj):
        super().__init__(obj, db_attribute_key="vitals")
        
    def initialize(self):
        """Set up HP and MP as Gauge Traits."""
        # 'max' for gauges is base + mod. We set base=100 for now.
        # This will be dynamically updated by derived properties.
        self.add("HP", "Health", trait_type="gauge", base=100, min=0)
        self.add("MP", "Mana", trait_type="gauge", base=100, min=0)

    def at_new_level(self, hp_gain, mp_gain):
        """Called by the ClassHandler during level-up."""
        self.HP.base += hp_gain
        self.MP.base += mp_gain
        # Refill vitals
        self.HP.current = self.HP.max
        self.MP.current = self.MP.max