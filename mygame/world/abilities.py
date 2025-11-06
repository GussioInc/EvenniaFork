# mygame/world/abilities.py
from evennia.scripts.scripts import DefaultScript
from evennia.contrib.rpg.buffs.buff import BaseBuff
import random

class BaseAbility:
    """
    Base class for all skills and spells.
    This is a "data" class, not a Typeclass.
    """
    key = "base_ability"
    mana_cost = 0
    cooldown_seconds = 0
    maintenance_cost = 0
    
    def __init__(self, caster):
        self.caster = caster

    def check_rules(self, target, **kwargs):
        """
        Check if the ability can be used.
        Returns (True, "OK") or (False, "Error Message").
        """
        if self.caster.vitals.MP.current < self.mana_cost:
            return (False, "You don't have enough mana.")
            
        # Check cooldown (using non-persistent attributes)
        if self.caster.ndb.cooldowns and \
           self.caster.ndb.cooldowns.get(self.key, 0) > 0:
            return (False, "That ability is not ready yet.")
            
        return (True, "OK")
        
    def pay_costs(self):
        """Deduct costs and set cooldowns."""
        self.caster.vitals.MP.current -= self.mana_cost
        
        if not self.caster.ndb.cooldowns:
            self.caster.ndb.cooldowns = {}
        self.caster.ndb.cooldowns[self.key] = self.cooldown_seconds
        
        from evennia.utils import delay
        
        def clear_cooldown(caster, key):
            if caster.ndb.cooldowns and key in caster.ndb.cooldowns:
                del caster.ndb.cooldowns[key]

        delay(self.cooldown_seconds, clear_cooldown, self.caster, self.key)

    def at_use(self, target, **kwargs):
        """
        The "payload" of the ability. Must be overridden.
        """
        raise NotImplementedError
    # mygame/world/abilities.py (continued)

class Fireball(BaseAbility):
    key = "fireball"
    mana_cost = 15
    cooldown_seconds = 6
    
    def at_use(self, target, **kwargs):
        """Execute the fireball."""
        caster = self.caster
        int_mod = (caster.stats.INT.value - 10) // 2
        damage = random.randint(1, 6) * caster.level + int_mod
        
        caster.msg(f"You hurl a fireball at {target.key}!")
        caster.location.msg_contents(
            f"{caster.key} hurls a fireball at {target.key}!",
            exclude=[caster, target]
        )
        target.msg(f"A fireball from {caster.key} engulfs you!")
        
        # Apply damage and aggro
        target.at_damage(damage, attacker=caster)

class MagicMissile(BaseAbility):
    key = "magic_missile"
    mana_cost = 5
    
    def at_use(self, target, **kwargs):
        """Execute the magic missile."""
        caster = self.caster
        int_mod = (caster.stats.INT.value - 10) // 2
        damage = random.randint(4, 8) + int_mod
        
        caster.msg(f"You send a crackling bolt of energy at {target.key}!")
        caster.location.msg_contents(
            f"{caster.key} sends a crackling bolt of energy at {target.key}!",
            exclude=[caster, target]
        )
        target.msg(f"A bolt of energy from {caster.key} strikes you!")
        
        target.at_damage(damage, attacker=caster)

class Bless(BaseAbility):
    key = "bless"
    mana_cost = 20
    maintenance_cost = 2
    
    def at_use(self, target, **kwargs):
        """Bless the target."""
        caster = self.caster
        caster.msg(f"You bless {target.key}.")
        if caster != target:
            target.msg(f"{caster.key} blesses you.")
        
        target.buffs.add("bless", duration=-1, to_hit=2, maintenance_cost=self.maintenance_cost)

class Poison(BaseAbility):
    key = "poison"
    mana_cost = 10
    
    def at_use(self, target, **kwargs):
        """Poison the target."""
        caster = self.caster
        caster.msg(f"You inflict a venomous poison on {target.key}.")
        target.msg(f"You have been poisoned by {caster.key}!")
        
        target.buffs.add("poison", duration=60, damage_per_tick=5, tick_rate=10)

class AcidRain(BaseAbility):
    key = "acid_rain"
    mana_cost = 40
    cooldown_seconds = 30
    
    def at_use(self, target, **kwargs):
        """Calls down a shower of acid on the room."""
        caster = self.caster
        room = caster.location
        
        caster.msg("|gYou call down a shower of corrosive acid!|n")
        room.msg_contents(
            f"|g{caster.key} calls down a shower of corrosive acid!|n",
            exclude=[caster]
        )
        
        int_mod = (caster.stats.INT.value - 10) // 2
        
        for char in room.contents:
            if char.is_typeclass("typeclasses.characters.Character") and char != caster:
                damage = random.randint(10, 20) + int_mod
                char.msg("|rAcid rain burns your skin!|n")
                char.at_damage(damage, attacker=caster)

class Dispel(BaseAbility):
    key = "dispel"
    mana_cost = 25
    
    def at_use(self, target, **kwargs):
        """Removes magical effects from the target."""
        caster = self.caster
        
        # get the buff to remove from the arguments
        buff_to_remove = kwargs.get("buff", "")
        if not buff_to_remove:
            caster.msg("Dispel what?")
            return
            
        if target.buffs.has(buff_to_remove):
            target.buffs.remove(buff_to_remove)
            caster.msg(f"You have dispelled {buff_to_remove} from {target.key}.")
            if caster != target:
                target.msg(f"{caster.key} has dispelled {buff_to_remove} from you.")
        else:
            caster.msg(f"{target.key} does not have the {buff_to_remove} buff.")

class Heal(BaseAbility):
    key = "heal"
    mana_cost = 10
    cooldown_seconds = 5
    
    def at_use(self, target, **kwargs):
        """Heals the target."""
        caster = self.caster
        int_mod = (caster.stats.INT.value - 10) // 2
        heal_amount = random.randint(15, 25) + int_mod
        
        # A proper implementation would use an `at_heal` hook
        # on the character. For simplicity, we'll modify vitals directly.
        target.vitals.HP.current += heal_amount
        if target.vitals.HP.current > target.vitals.HP.max:
            target.vitals.HP.current = target.vitals.HP.max
            
        caster.msg(f"|gYou heal {target.key} for {heal_amount} health.|n")
        if caster != target:
            target.msg(f"|g{caster.key} heals you for {heal_amount} health.|n")
        
        caster.location.msg_contents(
            f"{caster.key} heals {target.key}.",
            exclude=[caster, target]
        )

class ShieldOfFaith(BaseAbility):
    key = "shield of faith"
    mana_cost = 20
    maintenance_cost = 2
    
    def at_use(self, target, **kwargs):
        """Bolsters the target with a shield of faith."""
        caster = self.caster
        
        target.buffs.add("shield_of_faith", duration=-1, armor=5, maintenance_cost=self.maintenance_cost)
        caster.msg(f"You call upon a shield of faith to protect {target.key}.")
        if caster != target:
            target.msg(f"{caster.key} calls upon a shield of faith to protect you.")
