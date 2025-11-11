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
from evennia.contrib.rpg.equipment import EquipmentHandler

# Import Handlers (which we will create in Step 1.2)
from world.stats_handler import StatsHandler, VitalsHandler
from world.class_handler import ClassHandler
from world.race_handler import RaceHandler
from world.skill_handler import SkillHandler
from world.combat_handler import CharacterCombatHandler
from world.groups import Group

class GroupHandler:
    """Handles group mechanics for a character."""
    def __init__(self, character):
        self.character = character
        self.group = None  # Reference to the Group object

    @property
    def is_leader(self):
        return self.group and self.group.leader == self.character

    @property
    def is_in_group(self):
        return self.group is not None

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
    def race_handler(self):
        """Accesses the RaceHandler. Use: self.race_handler.get_race_obj()"""
        return RaceHandler(self)

    @lazy_property
    def skills(self):
        """Accesses the SkillHandler. Use: self.skills.execute("fireball")"""
        return SkillHandler(self)
    
    @lazy_property
    def combat(self):
        """Accesses the character's combat helper. Use: self.combat.target"""
        return CharacterCombatHandler(self)

    @lazy_property
    def group(self):
        """Accesses the character's group helper."""
        return GroupHandler(self)
        
    @lazy_property
    def buffs(self):
        """Accesses the BuffHandler contrib. Use: self.buffs.add(...)"""
        return BuffHandler(self)

    @lazy_property
    def equipment(self):
        """Accesses the EquipmentHandler. Use: self.equipment.wear()"""
        return EquipmentHandler(self, slots={
            "head": None,
            "finger1": None, "finger2": None,
            "neck1": None, "neck2": None,
            "hands": None,
            "arms": None,
            "chest": None,
            "about_waist": None,
            "legs": None,
            "feet": None,
            "about_body": None,
            "light": None,
            "shield": None,
            "wield1": None,
            "wrist1": None, "wrist2": None,
        })

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
        self.race_handler.initialize()
        self.skills.initialize()
        self.combat.initialize()
        self.equipment.initialize()
        
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
        # Check for damage reduction from buffs (like Armor spell)
        damage_reduction = self.buffs.get_total("damage_reduction", 0)
        amount -= damage_reduction
        if amount < 1:
            amount = 1  # Always do at least 1 damage

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

             if not attacker.group.is_in_group:
                 attacker.gain_exp(xp_value, source=self)
             else:
                 group = attacker.group.group
                 eligible_members = [
                     member for member in group.members
                     if member in attacker.combat.handler.db.participants
                     and member.location == attacker.location
                 ]

                 if not eligible_members:
                     # Fallback to the killer if no one else is eligible
                     attacker.gain_exp(xp_value, source=self)
                     return

                 xp_share = xp_value // len(eligible_members)
                 group.send_message(f"The group gains {xp_value} experience from the kill!")
                 for member in eligible_members:
                     member.gain_exp(xp_share, source=self)

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

    def at_post_move(self, source_location):
        """
        Called after a successful move.
        This is used to trigger followers to follow.
        """
        super().at_post_move(source_location)

        # See if anyone is following this character
        for follower in self.location.contents:
            if hasattr(follower, "ndb") and follower.ndb.follow_target == self:
                # The 'execute_cmd' will respect movement costs, delays, etc.
                follower.execute_cmd(f"goto {self.location.dbref}")
