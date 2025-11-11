# mygame/world/stats_handler.py
from evennia.contrib.rpg.traits import TraitHandler, Trait

class StatTrait(Trait):
    """A custom Trait class to enforce max stats."""
    def __set__(self, instance, value):
        """This is called when the trait's value is set."""
        race = instance.obj.race_handler.get_race_obj()
        max_stat = race.max_stats.get(self.key.upper(), 99)

        if value > max_stat:
            value = max_stat
            instance.obj.msg(f"Your {self.name} is maxed out at {max_stat}.")

        super().__set__(instance, value)

class StatsHandler(TraitHandler):
    """
    Manages the 6 core D&D stats using Static Traits.
    """
    def __init__(self, obj):
        """Uses a different attribute key to stay separate from vitals."""
        super().__init__(obj, db_attribute_key="stats")
        
    def initialize(self):
        """Called by Character.at_object_creation to set defaults."""
        self.add("STR", "Strength", trait_type="static", base=10, trait_class=StatTrait)
        self.add("DEX", "Dexterity", trait_type="static", base=10, trait_class=StatTrait)
        self.add("CON", "Constitution", trait_type="static", base=10, trait_class=StatTrait)
        self.add("INT", "Intelligence", trait_type="static", base=10, trait_class=StatTrait)
        self.add("WIS", "Wisdom", trait_type="static", base=10, trait_class=StatTrait)
        self.add("CHA", "Charisma", trait_type="static", base=10, trait_class=StatTrait)

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