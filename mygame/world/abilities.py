# mygame/world/abilities.py
from evennia.scripts.scripts import DefaultScript
from evennia.contrib.rpg.buffs.buff import BaseBuff
from evennia.utils import gametime
import random

class BaseAbility:
    """
    Base class for all skills and spells.
    This is a "data" class, not a Typeclass.
    """
    key = "base_ability"
    mana_cost = 0
    cooldown = 0  # In-game seconds
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
        self.caster.ndb.cooldowns[self.key] = self.cooldown
        
        from evennia.utils import delay
        
        def clear_cooldown(caster, key):
            if caster.ndb.cooldowns and key in caster.ndb.cooldowns:
                del caster.ndb.cooldowns[key]

        real_seconds = gametime.game_time_to_real_time(self.cooldown)
        delay(real_seconds, clear_cooldown, self.caster, self.key)

    def at_use(self, target, **kwargs):
        """
        The "payload" of the ability. Must be overridden.
        """
        raise NotImplementedError
    # mygame/world/abilities.py (continued)

class Fireball(BaseAbility):
    key = "fireball"
    mana_cost = 15
    cooldown = 288  # 6 seconds * 48
    
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
        
        target.buffs.add(
            "poison",
            duration=gametime.gametime(seconds=60),
            damage_per_tick=5,
            tick_rate=gametime.gametime(seconds=10)
        )

class AcidRain(BaseAbility):
    key = "acid_rain"
    mana_cost = 40
    cooldown = 1440  # 30 seconds * 48
    
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
    cooldown = 240  # 5 seconds * 48
    
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

class Bash(BaseAbility):
    key = "bash"
    cooldown = 480  # 10 seconds * 48

    def at_use(self, target, **kwargs):
        """Slam into the target, potentially stunning them."""
        caster = self.caster
        str_mod = (caster.stats.STR.value - 10) // 2
        damage = random.randint(1, 4) + str_mod

        caster.msg(f"You slam into {target.key}!")
        caster.location.msg_contents(
            f"{caster.key} slams into {target.key}!",
            exclude=[caster, target]
        )
        target.msg(f"{caster.key} slams into you!")

        target.at_damage(damage, attacker=caster)

        # Stun check
        if random.randint(1, 100) < 25 + (caster.level - target.level) * 5:
            target.msg("You are stunned!")
            target.buffs.add(
                "stun",
                duration=gametime.gametime(seconds=6),
                tick_rate=gametime.gametime(seconds=6),
                damage_per_tick=0
            )

class Kick(BaseAbility):
    key = "kick"
    cooldown = 240  # 5 seconds * 48

    def at_use(self, target, **kwargs):
        """A swift kick to the target."""
        caster = self.caster
        str_mod = (caster.stats.STR.value - 10) // 2
        damage = random.randint(1, 6) + str_mod

        caster.msg(f"You kick {target.key}!")
        caster.location.msg_contents(
            f"{caster.key} kicks {target.key}!",
            exclude=[caster, target]
        )
        target.msg(f"{caster.key} kicks you!")

        target.at_damage(damage, attacker=caster)

class Disarm(BaseAbility):
    key = "disarm"
    cooldown = 720  # 15 seconds * 48

    def at_use(self, target, **kwargs):
        """Attempt to disarm the target."""
        caster = self.caster

        # Success check
        if random.randint(1, 100) < 30 + (caster.level - target.level) * 5:
            target_weapon = target.equipment.slots.get("wield1")
            if target_weapon:
                target.equipment.remove(target_weapon)
                caster.msg(f"You disarm {target.key}!")
                target.msg(f"{caster.key} disarms you!")
            else:
                caster.msg(f"{target.key} is not wielding a weapon.")
        else:
            caster.msg(f"You fail to disarm {target.key}.")

class CriticalHit(BaseAbility):
    key = "critical_hit"

    def at_use(self, target, **kwargs):
        """Passive skill that grants a chance for extra damage."""
        target.buffs.add("critical_hit", duration=-1, damage_mod=1.5, chance=10)

class Berzerk(BaseAbility):
    key = "berzerk"
    cooldown = 8640  # 180 seconds * 48

    def at_use(self, target, **kwargs):
        """Go into a berzerk rage."""
        caster = self.caster
        caster.msg("You go into a berzerk rage!")
        caster.buffs.add("berzerk", duration=gametime.gametime(minutes=1), damage_mod=2, to_hit=-10)

class BurningHands(BaseAbility):
    key = "burning hands"
    mana_cost = 5

    def at_use(self, target, **kwargs):
        """A classic offensive spell."""
        caster = self.caster
        int_mod = (caster.stats.INT.value - 10) // 2
        damage = random.randint(1, 8) + int_mod

        caster.msg(f"You shoot a fan of flames at {target.key}!")
        target.at_damage(damage, attacker=caster)

class ChillTouch(BaseAbility):
    key = "chill touch"
    mana_cost = 5

    def at_use(self, target, **kwargs):
        """A touch of cold that weakens the target."""
        caster = self.caster
        int_mod = (caster.stats.INT.value - 10) // 2
        damage = random.randint(1, 4) + int_mod

        caster.msg(f"You touch {target.key} with a chilling hand!")
        target.at_damage(damage, attacker=caster)
        target.buffs.add("chill_touch", duration=gametime.gametime(minutes=2), STR=-2)

class Armor(BaseAbility):
    key = "armor"
    mana_cost = 10

    def at_use(self, target, **kwargs):
        """A magical shield that reduces incoming damage."""
        caster = self.caster
        caster.msg(f"You encase {target.key} in magical armor.")
        target.buffs.add("armor", duration=gametime.gametime(minutes=5), damage_reduction=5)

class Invisibility(BaseAbility):
    key = "invisibility"
    mana_cost = 15

    def at_use(self, target, **kwargs):
        """Render the target invisible."""
        caster = self.caster
        caster.msg(f"You fade {target.key} from sight.")
        target.buffs.add("invisibility", duration=gametime.gametime(minutes=5))
