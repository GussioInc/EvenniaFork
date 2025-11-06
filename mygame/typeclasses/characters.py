"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

# mygame/typeclasses/characters.py
from evennia import DefaultCharacter
from evennia.utils.utils import lazy_property
from evennia.contrib.rpg.buffs.buffhandler import BuffHandler

# Import Handlers (which we will create in Step 1.2)
from world.stats_handler import StatsHandler, VitalsHandler
from world.class_handler import ClassHandler
from world.skill_handler import SkillHandler
from world.combat_handler import CharacterCombatHandler

class Character(DefaultCharacter):
    """
    This is the base class for all player and non-player characters.
    It uses Handlers (attached via @lazy_property) to manage
    its various subsystems.
    """

    @lazy_property
    def stats(self):
        """Accesses the StatsHandler. Use: self.stats.str.value"""
        return StatsHandler(self)

    @lazy_property
    def vitals(self):
        """Accesses the VitalsHandler. Use: self.vitals.hp.current"""
        return VitalsHandler(self)

    @lazy_property
    def class_handler(self):
        """Accesses the ClassHandler. Use: self.class_handler.level"""
        return ClassHandler(self)

    @lazy_property
    def skills(self):
        """Accesses the SkillHandler. Use: self.skills.execute("fireball")"""
        return SkillHandler(self)
    
    @lazy_property
    def combat(self):
        """Accesses the character's combat helper. Use: self.combat.target"""
        return CharacterCombatHandler(self)
        
    @lazy_property
    def buffs(self):
        """Accesses the BuffHandler contrib. Use: self.buffs.add(...)"""
        return BuffHandler(self)

    def at_object_creation(self):
        """
        Called only once, when the object is first created.
        This is where we set up default stats, vitals, etc.
        """
        super().at_object_creation()
        # Initialize all handlers to set their default persistent data
        self.stats.initialize()
        self.vitals.initialize()
        self.class_handler.initialize()
        self.skills.initialize()
        self.combat.initialize()
        
        self.scripts.add("world.regen_script.RegenScript")

    @property
    def level(self):
        """Gets level from the class handler."""
        return self.class_handler.level

    @property
    def max_hp(self):
        """Calculates max HP based on class, level, and CON."""
        con_mod = (self.stats.CON.value - 10) // 2
        base_hp = self.class_handler.base_hp
        hp_per_level = self.class_handler.hp_per_level
        return base_hp + (self.level * (hp_per_level + con_mod))

    @property
    def max_mp(self):
        """Calculates max MP based on class, level, and INT/WIS."""
        prime_stat_mod = (self.stats.INT.value - 10) // 2 # (Example for Mage)
        base_mp = self.class_handler.base_mp
        mp_per_level = self.class_handler.mp_per_level
        return base_mp + (self.level * (mp_per_level + prime_stat_mod))

    def update_vitals_max(self):
        """
        Updates the TraitHandler gauges with new max values.
        Call this on level-up or when CON/INT changes.
        """
        if self.vitals.HP.max!= self.max_hp:
            self.vitals.HP.base = self.max_hp  # Gauge's 'max' is its 'base'
            # Optionally heal to full
            self.vitals.HP.current = self.vitals.HP.max
            
        if self.vitals.MP.max!= self.max_mp:
            self.vitals.MP.base = self.max_mp
            self.vitals.MP.current = self.vitals.MP.max

    def at_damage(self, amount, attacker=None):
        """
        Called when this character takes damage.
        """
        self.vitals.HP.current -= amount
        
        if attacker and self.combat.is_in_combat:
            # Add aggro to the handler
            handler = self.combat.handler
            if handler and not self.is_pc:
                # 'self' is an NPC, add hate for the 'attacker'
                handler.add_aggro(self, attacker, amount)

        if self.vitals.HP.current <= 0:
            self.at_defeat(attacker)
            
    def at_defeat(self, attacker=None):
        """Called when HP reaches 0."""
        self.msg("You have been defeated!")
        self.location.msg_contents(f"{self.key} falls to the ground, defeated.",
                                   exclude=self)
        
        if self.combat.is_in_combat:
            self.combat.handler.remove_combatant(self)
            
        # Grant XP to the attacker
        if attacker and not self.is_pc:
             xp_value = self.level * 100 # Example formula
             attacker.gain_exp(xp_value, source=self)

    def gain_exp(self, amount, source=None):
        """
        Called by other systems (CombatHandler, Quests)
        to grant experience to this character.
        
        This method is the *only* entry point for gaining XP,
        enforcing the Single Responsibility Principle.
        """
        if self.level >= 50: # Example max level
            return
            
        self.db.xp += amount
        self.msg(f"|gYou gain {amount} experience points from {source.key}!|n")
        
        # Delegate all level-up logic to the handler
        self.class_handler.check_for_level_up()
