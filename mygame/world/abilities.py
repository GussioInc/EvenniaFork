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
    key = "magic missile"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost."""
        self.mana_cost = round(2 + self.caster.level * 0.25)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Execute the magic missile."""
        caster = self.caster

        num_dice = 1 + caster.level // 8
        damage = sum(random.randint(1, 8) for _ in range(num_dice))
        
        caster.msg(f"You send a crackling bolt of energy at {target.key}!")
        target.msg(f"A bolt of energy from {caster.key} strikes you!")
        
        target.at_damage(damage, attacker=caster)

class Bless(BaseAbility):
    key = "bless"
    mana_cost = 8
    
    def at_use(self, target, **kwargs):
        """Bless the target."""
        caster = self.caster
        # 6 MUD hours * 75 seconds/hour
        duration_seconds = 6 * 75

        caster.msg(f"You cast 'bless' on {target.key}.")
        if caster != target:
            target.msg(f"{caster.key} casts 'bless' on you.")
        
        target.buffs.add(
            "bless",
            duration=gametime.gametime(seconds=duration_seconds),
            hitroll=2,
            magic_resistance=25
        )

class Poison(BaseAbility):
    key = "poison"
    mana_cost = 16
    
    def at_use(self, target, **kwargs):
        """Poisons the target, reducing their strength."""
        caster = self.caster
        duration_hours = caster.level / 2
        duration_seconds = duration_hours * 75
        str_debuff = -(caster.level // 7 + 1)

        caster.msg(f"You inflict a venomous poison on {target.key}.")
        target.msg(f"You have been poisoned by {caster.key}!")
        
        # TODO: Implement saving throws.
        target.buffs.add(
            "poison",
            duration=gametime.gametime(seconds=duration_seconds),
            STR=str_debuff
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
    mana_cost = 45
    
    def at_use(self, target, **kwargs):
        """Heals the target and cures blindness."""
        caster = self.caster
        heal_amount = sum(random.randint(1, 16) for _ in range(3)) + 100 + min(caster.level, 75)
        
        target.vitals.HP.current += heal_amount
        if target.vitals.HP.current > target.vitals.HP.max:
            target.vitals.HP.current = target.vitals.HP.max
            
        caster.msg(f"|gYou heal {target.key} for {heal_amount} health.|n")
        if caster != target:
            target.msg(f"|g{caster.key} heals you for {heal_amount} health.|n")

        if target.buffs.has("blindness"):
            target.buffs.remove("blindness")
            target.msg("Your vision returns!")

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
    cooldown = 4 * 48 # 4 rounds

    def at_use(self, target, **kwargs):
        """A powerful bash that can knock the target down."""
        caster = self.caster

        # TODO: Implement skill proficiency check
        if random.randint(1, 100) <= 75:
            damage = 10
            caster.msg(f"You bash {target.key}, knocking them to the ground!")
            target.msg(f"{caster.key} bashes you, knocking you to the ground!")
            target.at_damage(damage, attacker=caster)
            target.buffs.add(
                "stun",
                duration=gametime.gametime(seconds=4 * 6) # 4 rounds
            )
        else:
            caster.msg(f"You lose your balance while trying to bash {target.key} and fall down!")
            caster.buffs.add(
                "stun",
                duration=gametime.gametime(seconds=4 * 6) # 4 rounds
            )

class Kick(BaseAbility):
    key = "kick"
    cooldown = 5 * 48 # 5 seconds

    def at_use(self, target, **kwargs):
        """A swift kick to the target."""
        caster = self.caster

        # TODO: Implement skill proficiency check
        damage = caster.level * 2 + random.randint(1, 10)

        caster.msg(f"You kick {target.key}!")
        target.msg(f"{caster.key} kicks you!")

        target.at_damage(damage, attacker=caster)

class Disarm(BaseAbility):
    key = "disarm foe"
    cooldown = 15 * 48 # 15 seconds

    def at_use(self, target, **kwargs):
        """Attempt to disarm the target."""
        caster = self.caster

        # TODO: Implement skill proficiency check
        success_chance = 30 + (caster.level - target.level) * 5

        if random.randint(1, 100) <= success_chance:
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
    key = "critical hit"

    def at_use(self, target, **kwargs):
        """Passive skill that grants a chance for extra damage."""
        caster = self.caster
        caster.msg("You have learned to strike with critical force.")
        caster.buffs.add("critical_hit", duration=-1, damage_mod=1.5, chance=10)

class Berzerk(BaseAbility):
    key = "berzerk"
    cooldown = 180 * 48 # 180 seconds

    def at_use(self, target, **kwargs):
        """Go into a berzerk rage."""
        caster = self.caster
        caster.msg("You go into a berzerk rage!")
        caster.buffs.add("berzerk", duration=gametime.gametime(minutes=1), damage_mod=2, hitroll=-10)

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

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost."""
        self.mana_cost = round(6 + self.caster.level * 0.50)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """A touch of cold that weakens and damages the target."""
        caster = self.caster
        damage = random.randint(1, 12) + min(caster.level, 60)
        str_debuff = -(1 + caster.level // 7)
        duration_seconds = 4 * 75  # 4 MUD hours

        caster.msg(f"You touch {target.key} with a chilling hand!")
        target.msg(f"{caster.key}'s chilling touch weakens you!")

        # TODO: Implement saving throws to determine duration
        target.at_damage(damage, attacker=caster)
        target.buffs.add(
            "chill_touch",
            duration=gametime.gametime(seconds=duration_seconds),
            STR=str_debuff
        )

class Armor(BaseAbility):
    key = "armor"
    mana_cost = 12

    def at_use(self, target, **kwargs):
        """Improves the target's armor class."""
        caster = self.caster
        # 24 MUD hours * 75 seconds/hour
        duration_seconds = 24 * 75

        caster.msg(f"You cast 'armor' on {target.key}.")
        if caster != target:
            target.msg(f"{caster.key} casts 'armor' on you.")

        # A -20 AC in DikuMUD is a bonus. We'll represent this
        # as a +20 bonus in our "higher is better" system.
        target.buffs.add(
            "armor",
            duration=gametime.gametime(seconds=duration_seconds),
            ac=20
        )

class Invisibility(BaseAbility):
    key = "invisibility"
    mana_cost = 22

    def at_use(self, target, **kwargs):
        """Render the target invisible and grant an AC bonus."""
        caster = self.caster
        duration_hours = 12 + caster.level / 4
        duration_seconds = duration_hours * 75

        caster.msg(f"You fade {target.key} from sight.")
        if caster != target:
            target.msg(f"{caster.key} makes you invisible.")

        target.buffs.add(
            "invisibility",
            duration=gametime.gametime(seconds=duration_seconds),
            ac=40  # DikuMUD's -40 AC is a bonus
        )

# --- Placeholder Abilities ---

class Stab(BaseAbility): key = "stab"
class Bludgeon(BaseAbility): key = "bludgeon"
class Slash(BaseAbility): key = "slash"
class Chop(BaseAbility): key = "chop"
class Pierce(BaseAbility): key = "pierce"

class Scan(BaseAbility):
    key = "scan"

    def at_use(self, target, **kwargs):
        """Allows the user to see into adjacent rooms."""
        caster = self.caster
        caster.msg("You scan the area, but the feature is not yet implemented.")

class Caution(BaseAbility): key = "caution"

class Sneak(BaseAbility):
    key = "sneak"

    def at_use(self, target, **kwargs):
        """Allows the user to move silently."""
        caster = self.caster

        # TODO: Implement skill proficiency check
        if random.randint(1, 100) <= 75:
            caster.msg("You begin to move silently.")
            caster.buffs.add("sneak", duration=-1)
        else:
            caster.msg("You failed to move silently.")

class Swim(BaseAbility):
    key = "swim"

    def at_use(self, target, **kwargs):
        """Grants the ability to swim."""
        caster = self.caster
        caster.msg("You have learned how to swim.")
        caster.buffs.add("swim", duration=-1)

class PickLock(BaseAbility):
    key = "pick lock"

    def at_use(self, target, **kwargs):
        """Allows the user to attempt to pick a lock."""
        caster = self.caster
        caster.msg("You attempt to pick the lock, but it's not yet implemented.")

class Dodge(BaseAbility):
    key = "dodge"

    def at_use(self, target, **kwargs):
        """Grants a chance to dodge attacks."""
        caster = self.caster
        caster.msg("You have learned to dodge attacks.")
        caster.buffs.add("dodge", duration=-1, dodge_chance=10)

class Climb(BaseAbility):
    key = "climb"

    def at_use(self, target, **kwargs):
        """Grants the ability to climb."""
        caster = self.caster
        caster.msg("You have learned how to climb.")
        caster.buffs.add("climb", duration=-1)

class Hide(BaseAbility):
    key = "hide"

    def at_use(self, target, **kwargs):
        """Allows the user to hide from view."""
        caster = self.caster

        # TODO: Implement skill proficiency check
        if random.randint(1, 100) <= 75:
            caster.msg("You disappear into the shadows.")
            caster.buffs.add("hide", duration=-1)
        else:
            caster.msg("You failed to hide.")

class Throw(BaseAbility): key = "throw"
class SecondAttack(BaseAbility): key = "second attack"

class FirstAid(BaseAbility):
    key = "first aid"
    cooldown = 60 * 48 # 1 minute

    def at_use(self, target, **kwargs):
        """A simple heal to bring someone back from the brink of death."""
        caster = self.caster
        heal_amount = random.randint(10, 20)

        # TODO: Add check for incapacitated state
        caster.msg(f"You apply first aid to {target.key}.")
        target.msg(f"{caster.key} applies first aid to you.")

        target.vitals.HP.current += heal_amount
        if target.vitals.HP.current > target.vitals.HP.max:
            target.vitals.HP.current = target.vitals.HP.max

class Backstab(BaseAbility):
    key = "backstab"
    cooldown = 15 * 48 # 15 seconds

    def at_use(self, target, **kwargs):
        """A powerful attack from behind."""
        caster = self.caster

        # TODO: Implement skill proficiency and positional checks
        if random.randint(1, 100) <= 75:
            damage_multiplier = 2 + caster.level // 10
            base_damage = random.randint(1, 8) # Dagger damage
            damage = (base_damage + caster.damroll) * damage_multiplier

            caster.msg(f"You backstab {target.key}!")
            target.msg(f"{caster.key} backstabs you!")
            target.at_damage(damage, attacker=caster)
        else:
            caster.msg(f"You failed to backstab {target.key}.")

class UnfairFight(BaseAbility): key = "unfair fight"

class Bluff(BaseAbility):
    key = "bluff"
    cooldown = 10 * 48 # 10 seconds

    def at_use(self, target, **kwargs):
        """Temporarily stops combat with the target."""
        caster = self.caster

        # TODO: Implement skill proficiency check
        if random.randint(1, 100) <= 50:
            duration_rounds = random.randint(2, 5)
            caster.msg(f"You bluff {target.key}, confusing them!")
            target.msg(f"{caster.key} bluffs you, leaving you confused!")
            target.buffs.add(
                "stun",
                duration=gametime.gametime(seconds=duration_rounds * 6)
            )
        else:
            caster.msg(f"Your bluff against {target.key} fails.")

class Steal(BaseAbility):
    key = "steal"
    cooldown = 30 * 48 # 30 seconds

    def at_use(self, target, **kwargs):
        """Attempts to steal an item from the target."""
        caster = self.caster

        # This will be passed from the command
        item_to_steal = kwargs.get("item", "")

        # TODO: Implement skill proficiency check and PK checks
        if random.randint(1, 100) <= 50:
            item = target.search(item_to_steal, location=target)
            if item:
                item.move_to(caster)
                caster.msg(f"You steal {item.key} from {target.key}.")
                target.msg(f"{caster.key} steals {item.key} from you!")
            else:
                caster.msg(f"{target.key} does not have that item.")
        else:
            caster.msg(f"You failed to steal from {target.key}.")

class Escape(BaseAbility):
    key = "escape"
    cooldown = 30 * 48 # 30 seconds

    def at_use(self, target, **kwargs):
        """Allows the user to attempt to flee combat without penalty."""
        caster = self.caster

        # TODO: Implement skill proficiency check
        if random.randint(1, 100) <= 50:
            caster.msg("You successfully escape from combat!")
            caster.combat.end_combat()
        else:
            caster.msg("You failed to escape!")

class Tumble(BaseAbility): key = "tumble"

class Blindfight(BaseAbility):
    key = "blindfight"

    def at_use(self, target, **kwargs):
        """Grants the ability to fight while blinded."""
        caster = self.caster
        caster.msg("You have learned to fight without your eyes.")
        caster.buffs.add("blindfight", duration=-1)

class RidingLandbased(BaseAbility): key = "riding landbased"
class FanOfKnives(BaseAbility): key = "fan of knives"
class EliteBluff(BaseAbility): key = "elite bluff"
class Stun(BaseAbility): key = "stun"
class DisarmFoe(BaseAbility): key = "disarm foe"
class PoisonBlade(BaseAbility): key = "poison blade"
class SenseStealth(BaseAbility): key = "sense stealth"
class DualWeapons(BaseAbility): key = "dual weapons"

class Parrying(BaseAbility):
    key = "parrying"

    def at_use(self, target, **kwargs):
        """Grants a chance to parry attacks."""
        caster = self.caster
        caster.msg("You have learned to parry attacks.")
        caster.buffs.add("parrying", duration=-1, parry_chance=10)

class MountedBattle(BaseAbility): key = "mounted battle"
class ElitePoisonBlade(BaseAbility): key = "elite poison blade"
class Scout(BaseAbility): key = "scout"
class FirstToAttack(BaseAbility): key = "first to attack"

class Legsweep(BaseAbility):
    key = "legsweep"
    cooldown = 10 * 48 # 10 seconds

    def at_use(self, target, **kwargs):
        """Sweeps the target's legs, causing them to fall."""
        caster = self.caster

        # TODO: Implement skill proficiency check
        if random.randint(1, 100) <= 75:
            damage = caster.stats.STR.value * 2
            caster.msg(f"You sweep {target.key}'s legs out from under them!")
            target.msg(f"{caster.key} sweeps your legs out from under you!")
            target.at_damage(damage, attacker=caster)
            target.buffs.add("stun", duration=gametime.gametime(seconds=2 * 6)) # 2 rounds
            target.buffs.add("infuriated", duration=-1)
        else:
            caster.msg("You fail to sweep the legs of {target.key}.")

class Taunt(BaseAbility):
    key = "taunt"

    def at_use(self, target, **kwargs):
        """Taunts a target in an adjacent room."""
        caster = self.caster
        caster.msg(f"You attempt to taunt {target.key}, but it's not yet implemented.")

class ThirdAttack(BaseAbility):
    key = "third attack"

    def at_use(self, target, **kwargs):
        """A passive skill that grants a chance for a third attack."""
        caster = self.caster
        caster.msg("You have learned to make a third attack.")
        caster.buffs.add("third_attack", duration=-1, extra_attacks=1)

class NeutralizePoison(BaseAbility):
    key = "neutralize poison"

    def at_use(self, target, **kwargs):
        """Removes poison from the target."""
        caster = self.caster

        if target.buffs.has("poison"):
            target.buffs.remove("poison")
            caster.msg(f"You neutralize the poison in {target.key}.")
            if caster != target:
                target.msg(f"{caster.key} neutralizes the poison in you.")
        else:
            caster.msg(f"{target.key} is not poisoned.")

class KickDirt(BaseAbility):
    key = "kick dirt"
    cooldown = 10 * 48 # 10 seconds

    def at_use(self, target, **kwargs):
        """Kicks dirt in the target's face, stunning them."""
        caster = self.caster

        # TODO: Implement skill proficiency check
        if random.randint(1, 100) <= 75:
            damage = 10
            caster.msg(f"You kick dirt in {target.key}'s face!")
            target.msg(f"{caster.key} kicks dirt in your face, blinding you!")
            target.at_damage(damage, attacker=caster)
            target.buffs.add(
                "stun",
                duration=gametime.gametime(seconds=3 * 6) # 3 rounds
            )
        else:
            caster.msg("You kick dirt, but miss and fall on your arse!")
            caster.buffs.add(
                "stun",
                duration=gametime.gametime(seconds=3 * 6) # 3 rounds
            )

class Track(BaseAbility):
    key = "track"

    def at_use(self, target, **kwargs):
        """Allows the user to track a target."""
        caster = self.caster
        caster.msg(f"You attempt to track {target.key}, but it's not yet implemented.")

class CircleAround(BaseAbility):
    key = "circle around"
    cooldown = 6 * 48 # 6 seconds, placeholder for round-based delays

    def check_rules(self, target, **kwargs):
        """Skill can only be used in combat."""
        if not self.caster.combat.is_in_combat:
            return (False, "You can only circle around an opponent in combat.")
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """A powerful attack from the side."""
        caster = self.caster

        # TODO: Implement skill proficiency and proper delay system
        if random.randint(1, 100) <= 75:
            damage_multiplier = 2 + caster.level // 10
            base_damage = random.randint(1, 8) # Dagger damage
            damage = (base_damage + caster.damroll) * damage_multiplier

            caster.msg(f"You circle around {target.key} and strike!")
            target.msg(f"{caster.key} circles around you and strikes!")
            target.at_damage(damage, attacker=caster)
        else:
            caster.msg(f"You failed to circle around {target.key}.")

class ThievesGuild(BaseAbility):
    key = "thieves guild"

    def at_use(self, target, **kwargs):
        """A passive skill for thieves."""
        caster = self.caster
        caster.msg("You have learned the ways of the Thieves Guild.")
        caster.buffs.add("thieves_guild", duration=-1)

class Push(BaseAbility):
    key = "push"

    def at_use(self, target, **kwargs):
        """Pushes the target to an adjacent room."""
        caster = self.caster
        caster.msg(f"You attempt to push {target.key}, but it's not yet implemented.")

class ExtraDamage(BaseAbility):
    key = "extra damage"

    def at_use(self, target, **kwargs):
        """A passive skill that grants extra damage."""
        caster = self.caster
        caster.msg("You have learned to deal extra damage.")
        caster.buffs.add("extra_damage", duration=-1, damroll=2)

class Assassinate(BaseAbility):
    key = "assassinate"
    cooldown = 30 * 48 # 30 seconds

    def at_use(self, target, **kwargs):
        """A powerful attack that can halve the target's health."""
        caster = self.caster

        # TODO: Implement skill proficiency check
        if random.randint(1, 100) <= 50:
            damage = target.vitals.HP.current // 2
            caster.msg(f"You assassinate {target.key}!")
            target.msg(f"{caster.key} assassinates you!")
            target.at_damage(damage, attacker=caster)
        else:
            caster.msg(f"You failed to assassinate {target.key}.")

class RidingAirborne(BaseAbility): key = "riding airborne"
class Ambush(BaseAbility): key = "ambush"
class Preparation(BaseAbility): key = "preparation"
class LethalBlow(BaseAbility): key = "lethal blow"
class EliteBackstab(BaseAbility): key = "elite backstab"
class ReverseVitalizeSta(BaseAbility): key = "reverse vitalize sta"
class Spellcasting(BaseAbility): key = "spellcasting"

class Rescue(BaseAbility):
    key = "rescue"

    def at_use(self, target, **kwargs):
        """Allows the user to rescue another character from an attack."""
        caster = self.caster
        caster.msg(f"You attempt to rescue {target.key}, but it's not yet implemented.")

class Spellcraft(BaseAbility): key = "spellcraft"
class TwoHandedWeapon(BaseAbility): key = "two-handed weapon"
class BattleTactics(BaseAbility): key = "battle tactics"

class Bashdoor(BaseAbility):
    key = "bashdoor"

    def at_use(self, target, **kwargs):
        """Allows the user to attempt to break down a door."""
        caster = self.caster
        caster.msg("You attempt to bash the door down, but it's not yet implemented.")

class Smite(BaseAbility): key = "smite"
class HeroicRescue(BaseAbility): key = "heroic rescue"
class VitalizeMana(BaseAbility): key = "vitalize mana"
class VitalizeStamina(BaseAbility): key = "vitalize stamina"

class ShieldBlock(BaseAbility):
    key = "shield block"

    def at_use(self, target, **kwargs):
        """Grants a chance to block attacks with a shield."""
        caster = self.caster
        caster.msg("You have learned to block attacks with your shield.")
        caster.buffs.add("shield_block", duration=-1, shield_block_chance=10)

class Wrath(BaseAbility): key = "wrath"
class ShieldBash(BaseAbility): key = "shield bash"
class ReverseVitalizeMan(BaseAbility): key = "reverse vitalize man"
class SenseTraps(BaseAbility): key = "sense traps"
class ReadEssence(BaseAbility): key = "read essence"
class PsychicBlast(BaseAbility): key = "psychic blast"

class Accuracy(BaseAbility):
    key = "accuracy"
    mana_cost = 25

    def at_use(self, target, **kwargs):
        """Increases the target's hitroll."""
        caster = self.caster
        duration_hours = caster.level / 2
        # MUD hours are 75 seconds.
        duration_seconds = duration_hours * 75

        caster.msg(f"You cast 'accuracy' on {target.key}.")
        if caster != target:
            target.msg(f"{caster.key} casts 'accuracy' on you.")

        target.buffs.add(
            "accuracy",
            duration=gametime.gametime(seconds=duration_seconds),
            hitroll=4
        )

class SummonMount(BaseAbility): key = "summon mount"

class DivineStorm(BaseAbility):
    key = "divine storm"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost based on targets."""
        room = self.caster.location
        num_targets = len([
            char for char in room.contents
            if not char.is_pc and char != self.caster
        ])

        self.mana_cost = round(1 + (4 + self.caster.level * 0.50) * num_targets)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Strikes all MOBs in the room with divine power."""
        caster = self.caster
        room = caster.location
        damage = caster.vitals.HP.max

        caster.msg("You call down a divine storm!")
        room.msg_contents(
            f"{caster.key} calls down a divine storm!",
            exclude=[caster]
        )

        for char in room.contents:
            if not char.is_pc and char != caster:
                char.msg("The divine storm strikes you!")
                # TODO: Implement saving throws.
                char.at_damage(damage, attacker=caster)

class DetectEvil(BaseAbility):
    key = "detect evil"
    mana_cost = 12

    def at_use(self, target, **kwargs):
        """Allows the caster to detect evil alignment."""
        caster = self.caster
        # Duration is 12 + level MUD hours. MUD hours are 75 seconds.
        duration_seconds = (12 + caster.level) * 75

        caster.msg("You cast 'detect evil'. Your eyes tingle.")

        # A buff is used to signify the ongoing effect.
        # Other systems (like the `look` command) would check for this buff.
        caster.buffs.add(
            "detect_evil",
            duration=gametime.gametime(seconds=duration_seconds)
        )

class CureLight(BaseAbility):
    key = "cure light"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost."""
        self.mana_cost = round(2 + self.caster.level * 0.50)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Heals a light amount of damage."""
        caster = self.caster

        num_dice = 1 + caster.level // 6
        heal_amount = sum(random.randint(1, 6) for _ in range(num_dice)) + caster.level

        target.vitals.HP.current += heal_amount
        if target.vitals.HP.current > target.vitals.HP.max:
            target.vitals.HP.current = target.vitals.HP.max

        caster.msg(f"|gYou heal {target.key} for {heal_amount} health.|n")
        if caster != target:
            target.msg(f"|g{caster.key} heals you for {heal_amount} health.|n")

class DispelEvil(BaseAbility):
    key = "dispel evil"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost."""
        self.mana_cost = round(1 + self.caster.level * 0.50)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Damages evil targets, with a risk to an evil caster."""
        caster = self.caster
        damage = target.vitals.HP.max // 2

        # Using alignment: > 350 is good, < -350 is evil
        caster_is_evil = caster.db.alignment < -350
        target_is_evil = target.db.alignment < -350

        if caster_is_evil:
            caster.msg("Your evil prayer backfires!")
            caster.at_damage(damage, attacker=caster)
        elif target_is_evil:
            caster.msg(f"You call upon holy power to smite {target.key}!")
            target.msg(f"{caster.key}'s holy power smites you!")
            target.at_damage(damage, attacker=caster)
        else:
            caster.msg("The magic fizzles, having no effect.")

class DetectMagic(BaseAbility):
    key = "detect magic"
    mana_cost = 50

    def at_use(self, target, **kwargs):
        """Allows the target to see magical auras."""
        caster = self.caster
        # Duration is max(20, level) MUD minutes. MUD minutes are 60 seconds.
        duration_minutes = max(20, caster.level)
        duration_seconds = duration_minutes * 60

        caster.msg(f"You cast 'detect magic' on {target.key}.")
        if caster != target:
            target.msg(f"{caster.key}'s magic enhances your vision.")
        else:
            caster.msg("Your eyes tingle as you sense for magic.")

        target.buffs.add(
            "detect_magic",
            duration=gametime.gametime(seconds=duration_seconds)
        )

class DetectInvisibility(BaseAbility): key = "detect invisibility"
class WordOfHealing(BaseAbility): key = "word of healing"

class ProtectionFromEvil(BaseAbility):
    key = "protection from evil"
    mana_cost = 16

    def at_use(self, target, **kwargs):
        """Protects the caster with a holy aura."""
        caster = self.caster
        # 24 MUD hours * 75 seconds/hour
        duration_seconds = 24 * 75

        caster.msg("A holy aura surrounds you.")

        # Simplified: grants a general AC bonus instead of vs. evil
        caster.buffs.add(
            "protection_from_evil",
            duration=gametime.gametime(seconds=duration_seconds),
            ac=20
        )

class Haste(BaseAbility):
    key = "haste"
    mana_cost = 100

    def at_use(self, target, **kwargs):
        """Increases the caster's attack speed."""
        caster = self.caster
        duration_seconds = 1 * 75  # 1 MUD hour

        caster.msg("You feel yourself moving faster!")

        caster.buffs.add(
            "haste",
            duration=gametime.gametime(seconds=duration_seconds),
            extra_attacks=1
        )

class CureBlind(BaseAbility):
    key = "cure blind"
    mana_cost = 14

    def at_use(self, target, **kwargs):
        """Cures blindness."""
        caster = self.caster

        if target.buffs.has("blindness"):
            target.buffs.remove("blindness")
            caster.msg(f"You cure {target.key}'s blindness.")
            if caster != target:
                target.msg(f"{caster.key} cures your blindness.")
        else:
            caster.msg(f"{target.key} is not blind.")

class CreateFood(BaseAbility):
    key = "create food"
    mana_cost = 15

    def at_use(self, target, **kwargs):
        """Creates a piece of magical food."""
        from evennia import create_object

        caster = self.caster

        food = create_object(
            "typeclasses.objects.Object",
            key="a piece of waybread",
            location=caster,
            attributes={
                "desc": "A piece of freshly made waybread. It looks delicious."
            }
        )

        caster.msg(f"You create {food.key}!")

class CureCritic(BaseAbility):
    key = "cure critic"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost."""
        self.mana_cost = round(12 + self.caster.level * 0.47)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Heals a critical amount of damage."""
        caster = self.caster

        num_dice = 3 + caster.level // 8
        heal_amount = sum(random.randint(1, 16) for _ in range(num_dice)) + caster.level

        target.vitals.HP.current += heal_amount
        if target.vitals.HP.current > target.vitals.HP.max:
            target.vitals.HP.current = target.vitals.HP.max

        caster.msg(f"|gYou heal {target.key} for {heal_amount} health.|n")
        if caster != target:
            target.msg(f"|g{caster.key} heals you for {heal_amount} health.|n")

class Summon(BaseAbility): key = "summon"
class Relocate(BaseAbility): key = "relocate"

class RemovePoison(BaseAbility):
    key = "remove poison"
    mana_cost = 14

    def at_use(self, target, **kwargs):
        """Removes poison from the target."""
        caster = self.caster

        if target.buffs.has("poison"):
            target.buffs.remove("poison")
            caster.msg(f"You remove the poison from {target.key}.")
            if caster != target:
                target.msg(f"{caster.key} removes the poison from you.")
        else:
            caster.msg(f"{target.key} is not poisoned.")

class RemoveCurse(BaseAbility):
    key = "remove curse"
    mana_cost = 14

    def at_use(self, target, **kwargs):
        """Removes a curse from the target."""
        caster = self.caster

        if target.buffs.has("curse"):
            target.buffs.remove("curse")
            caster.msg(f"You remove the curse from {target.key}.")
            if caster != target:
                target.msg(f"{caster.key} removes the curse from you.")
        else:
            caster.msg(f"{target.key} is not cursed.")

class SenseLife(BaseAbility):
    key = "sense life"
    mana_cost = 13

    def at_use(self, target, **kwargs):
        """Allows the caster to sense hidden life."""
        caster = self.caster
        duration_hours = caster.level
        duration_seconds = duration_hours * 75

        caster.msg("Your awareness of your surroundings sharpens.")

        caster.buffs.add(
            "sense_life",
            duration=gametime.gametime(seconds=duration_seconds)
        )

class TurnUndead(BaseAbility): key = "turn undead"
class ChargeWand(BaseAbility): key = "charge wand"

class Sanctuary(BaseAbility):
    key = "sanctuary"
    mana_cost = 50

    def at_use(self, target, **kwargs):
        """Halves incoming damage to the target."""
        caster = self.caster
        duration_hours = 4
        duration_seconds = duration_hours * 75

        caster.msg(f"A shimmering aura surrounds {target.key}.")
        if caster != target:
            target.msg(f"{caster.key} surrounds you with a shimmering aura.")

        target.buffs.add(
            "sanctuary",
            duration=gametime.gametime(seconds=duration_seconds),
            damage_reduction_percent=0.5
        )

class GroupHeal(BaseAbility):
    key = "group heal"

    def check_rules(self, target, **kwargs):
        """Check mana cost based on group members in the room."""
        caster = self.caster
        if not caster.group.is_in_group:
            return (False, "You are not in a group.")

        num_targets = len([
            member for member in caster.group.group.members
            if member.location == caster.location
        ])

        self.mana_cost = round(25 + (10 + caster.level * 0.25) * num_targets)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Heals all group members in the room."""
        caster = self.caster
        heal_amount = sum(random.randint(1, 16) for _ in range(3)) + 100 + min(caster.level, 75)

        caster.msg("|gYou cast 'group heal'!|n")

        for member in caster.group.group.members:
            if member.location == caster.location:
                member.vitals.HP.current += heal_amount
                if member.vitals.HP.current > member.vitals.HP.max:
                    member.vitals.HP.current = member.vitals.HP.max

                if member != caster:
                    member.msg(f"|g{caster.key} heals you for {heal_amount} health!|n")
                else:
                    member.msg(f"|gYou heal yourself for {heal_amount} health.|n")

class DivineWrath(BaseAbility):
    key = "divine wrath"
    mana_cost = 20

    def at_use(self, target, **kwargs):
        """Fills the target with divine wrath, boosting stats."""
        caster = self.caster
        # 6 MUD hours * 75 seconds/hour
        duration_seconds = 6 * 75

        caster.msg(f"You cast 'divine wrath' on {target.key}.")
        if caster != target:
            target.msg(f"{caster.key} fills you with divine wrath!")

        target.buffs.add(
            "divine_wrath",
            duration=gametime.gametime(seconds=duration_seconds),
            CON=10,
            STR=10,
            CHA=10
        )

class Regeneration(BaseAbility): key = "regeneration"
class MysticShield(BaseAbility): key = "mystic shield"
class LayOnHands(BaseAbility): key = "lay on hands"
class MartialArts(BaseAbility): key = "martial arts"
class QuiveringPalm(BaseAbility): key = "quivering palm"
class SpinKick(BaseAbility): key = "spin kick"
class Pugilism(BaseAbility): key = "pugilism"
class Tumble(BaseAbility): key = "tumble"
class Meditate(BaseAbility): key = "meditate"
class FourthAttack(BaseAbility): key = "fourth attack"
class Strike(BaseAbility): key = "strike"
class Jab(BaseAbility): key = "jab"
class FifthAttack(BaseAbility): key = "fifth attack"

class ProtectionFromGood(BaseAbility):
    key = "protection from good"
    mana_cost = 16

    def at_use(self, target, **kwargs):
        """Protects the caster with an unholy aura."""
        caster = self.caster
        # 24 MUD hours * 75 seconds/hour
        duration_seconds = 24 * 75

        caster.msg("An unholy aura surrounds you.")

        # Simplified: grants a general AC bonus instead of vs. good
        caster.buffs.add(
            "protection_from_good",
            duration=gametime.gametime(seconds=duration_seconds),
            ac=20
        )

class FleshRestore(BaseAbility): key = "flesh restore"

class Blindness(BaseAbility):
    key = "blindness"
    mana_cost = 13

    def check_rules(self, target, **kwargs):
        """Spell fails if target is higher level."""
        if target.level > self.caster.level:
            return (False, "Your target is too powerful to blind.")
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Blinds the target, reducing hitroll and increasing AC."""
        caster = self.caster
        # 2 MUD hours * 75 seconds/hour
        duration_seconds = 2 * 75

        caster.msg(f"You cast 'blindness' on {target.key}.")
        if caster != target:
            target.msg(f"{caster.key} casts 'blindness' on you. You can't see!")

        # TODO: Implement saving throws.
        # The "blinds the target" effect is represented by the buff itself.
        # Combat systems can check for `target.buffs.has("blindness")`.
        target.buffs.add(
            "blindness",
            duration=gametime.gametime(seconds=duration_seconds),
            hitroll=-4,
            ac=40
        )

class DetectPoison(BaseAbility):
    key = "detect poison"
    mana_cost = 24

    def at_use(self, target, **kwargs):
        """Checks if the target is poisoned."""
        caster = self.caster

        # This assumes that a "poison" buff exists.
        if target.buffs.has("poison"):
            caster.msg(f"You sense a venomous poison within {target.key}.")
        else:
            caster.msg(f"{target.key} appears to be free of poison.")

class Strength(BaseAbility):
    key = "strength"
    mana_cost = 25

    def at_use(self, target, **kwargs):
        """Increases the target's strength."""
        caster = self.caster
        duration_hours = 4 + caster.level / 2
        duration_seconds = duration_hours * 75

        str_bonus = 2 if caster.level >= 19 else 1

        caster.msg(f"You cast 'strength' on {target.key}.")
        if caster != target:
            target.msg(f"{caster.key} makes you feel stronger.")

        # This buff is "stackable" by default in the buff handler
        target.buffs.add(
            "strength",
            duration=gametime.gametime(seconds=duration_seconds),
            STR=str_bonus
        )

class DetectGood(BaseAbility):
    key = "detect good"
    mana_cost = 12

    def at_use(self, target, **kwargs):
        """Allows the caster to detect good alignment."""
        caster = self.caster
        # Duration is 12 + level MUD hours. MUD hours are 75 seconds.
        duration_seconds = (12 + caster.level) * 75

        caster.msg("You cast 'detect good'. Your eyes tingle.")

        caster.buffs.add(
            "detect_good",
            duration=gametime.gametime(seconds=duration_seconds)
        )

class FleshAnew(BaseAbility): key = "flesh anew"
class LocateObject(BaseAbility): key = "locate object"

class WordOfRecall(BaseAbility):
    key = "word of recall"
    mana_cost = 30

    def at_use(self, target, **kwargs):
        """Transports the caster to their home."""
        caster = self.caster
        caster.msg("You utter a word of recall.")
        caster.move_to(caster.home)

class Fly(BaseAbility):
    key = "fly"
    mana_cost = 40

    def at_use(self, target, **kwargs):
        """Grants the target the ability to fly."""
        caster = self.caster
        duration_hours = 10 + caster.level / 10
        duration_seconds = duration_hours * 75

        caster.msg(f"You grant {target.key} the ability to fly.")
        if caster != target:
            target.msg(f"{caster.key} grants you the ability to fly.")

        target.buffs.add(
            "fly",
            duration=gametime.gametime(seconds=duration_seconds)
        )

class Dexterity(BaseAbility): key = "dexterity"
class Portal(BaseAbility): key = "portal"
class MysticalCoat(BaseAbility): key = "mystical coat"
class Charisma(BaseAbility): key = "charisma"

class Earthquake(BaseAbility):
    key = "earthquake"

    def check_rules(self, target, **kwargs):
        """Check mana cost based on targets."""
        room = self.caster.location
        num_targets = len([
            char for char in room.contents
            if not char.is_pc and char != self.caster
        ])

        self.mana_cost = 25 + 6 * num_targets
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Shakes the earth, damaging all MOBs in the room."""
        caster = self.caster
        room = caster.location

        damage = sum(random.randint(1, 16) for _ in range(8)) + min(caster.level, 70)

        caster.msg("The earth shakes violently!")
        room.msg_contents(
            f"The earth shakes violently as {caster.key} casts 'earthquake'!",
            exclude=[caster]
        )

        for char in room.contents:
            if not char.is_pc and char != caster:
                char.msg("You are shaken by the earthquake!")
                char.at_damage(damage, attacker=caster)

class EnergyDrain(BaseAbility):
    key = "energy drain"
    mana_cost = 24

    def at_use(self, target, **kwargs):
        """Drains energy from the target, with damage scaling by level."""
        caster = self.caster

        level_diff = caster.level - target.level

        if target.level < caster.level / 3:
            damage = target.vitals.HP.max // 3
        elif target.level < caster.level * 2 / 3:
            damage = target.vitals.HP.max // 6
        else:
            damage = random.randint(1, 20)

        caster.msg(f"You drain energy from {target.key}!")
        target.msg(f"{caster.key} drains your energy!")

        # TODO: Implement saving throws.
        target.at_damage(damage, attacker=caster)

class ThornBlast(BaseAbility): key = "thorn blast"
class CatEyes(BaseAbility): key = "cat eyes"
class ShockingSphere(BaseAbility): key = "shocking sphere"
class Rejuvenation(BaseAbility): key = "rejuvenation"
class StarFlare(BaseAbility): key = "star flare"
class Frostbite(BaseAbility): key = "frostbite"
class EnchantWeapon(BaseAbility): key = "enchant weapon"
class FlameBlade(BaseAbility): key = "flame blade"
class Infravision(BaseAbility): key = "infravision"

class Harm(BaseAbility):
    key = "harm"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost."""
        self.mana_cost = round(16 + self.caster.level * 0.125)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Inflicts a harmful amount of damage."""
        caster = self.caster

        num_dice = 16 + caster.level // 16
        damage = sum(random.randint(1, 8) for _ in range(num_dice))

        caster.msg(f"You inflict grievous harm upon {target.key}!")
        target.msg(f"{caster.key} harms you!")

        # TODO: Implement saving throws.
        target.at_damage(damage, attacker=caster)

class RechargeLight(BaseAbility): key = "recharge light"
class Entangle(BaseAbility): key = "entangle"
class Levitation(BaseAbility): key = "levitation"
class Fog(BaseAbility): key = "fog"
class CharmPerson(BaseAbility): key = "charm person"
class Identify(BaseAbility): key = "identify"
class Slow(BaseAbility): key = "slow"
class Fear(BaseAbility): key = "fear"

class GroupRecall(BaseAbility):
    key = "group recall"

    def check_rules(self, target, **kwargs):
        """Check mana cost based on group members in the room."""
        caster = self.caster
        if not caster.group.is_in_group:
            return (False, "You are not in a group.")

        num_targets = len([
            member for member in caster.group.group.members
            if member.location == caster.location
        ])

        self.mana_cost = round(15 + (10 + caster.level * 0.25) * num_targets)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Recalls all group members in the room to the caster's home."""
        caster = self.caster

        caster.msg("You cast 'group recall'!")

        for member in caster.group.group.members:
            if member.location == caster.location:
                member.move_to(caster.home)
                if member != caster:
                    member.msg(f"{caster.key} recalls you to their home.")

class WizardShield(BaseAbility): key = "wizard shield"

class AcidBlast(BaseAbility):
    key = "acid blast"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost."""
        self.mana_cost = round(27 + self.caster.level * 0.18)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Hurls a blast of acid at the target."""
        caster = self.caster

        num_dice = 8 + caster.level // 26
        damage = sum(random.randint(1, 10) for _ in range(num_dice)) + 40

        caster.msg(f"You hurl a blast of acid at {target.key}!")
        caster.location.msg_contents(
            f"{caster.key} hurls a blast of acid at {target.key}!",
            exclude=[caster, target]
        )
        target.msg(f"A blast of acid from {caster.key} strikes you!")

        # TODO: Implement saving throws.
        target.at_damage(damage, attacker=caster)

class VorpalPlating(BaseAbility): key = "vorpal plating"
class DireBearForm(BaseAbility): key = "dire bear form"
class Rimefang(BaseAbility): key = "rimefang"
class GroupRelocate(BaseAbility): key = "group relocate"
class Flood(BaseAbility): key = "flood"
class DireWolfForm(BaseAbility): key = "dire wolf form"
class Blaze(BaseAbility): key = "blaze"
class MageGauntlets(BaseAbility): key = "mage gauntlets"

class LightningBreath(BaseAbility):
    key = "lightning breath"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost based on targets."""
        room = self.caster.location
        num_targets = len([
            char for char in room.contents
            if not char.is_pc and char != self.caster
        ])

        self.mana_cost = round(1 + (4 + self.caster.level * 0.50) * num_targets)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Breathes lightning on all MOBs in the room."""
        caster = self.caster
        room = caster.location

        if caster.vitals.HP.current < 200:
            damage = 100 + random.randint(1, 100)
        else:
            damage = 100 + random.randint(1, caster.vitals.HP.current - 100)

        caster.msg("You breathe a cone of lightning!")
        room.msg_contents(
            f"{caster.key} breathes a cone of lightning!",
            exclude=[caster]
        )

        for char in room.contents:
            if not char.is_pc and char != caster:
                char.msg("The lightning breath shocks you!")
                # TODO: Implement saving throws.
                char.at_damage(damage, attacker=caster)

class Cyclone(BaseAbility): key = "cyclone"
class Smash(BaseAbility): key = "smash"
class DireStrike(BaseAbility): key = "dire strike"
class Swipe(BaseAbility): key = "swipe"
class Fade(BaseAbility): key = "fade"
class FlankAttack(BaseAbility): key = "flank attack"
class FuriousHowl(BaseAbility): key = "furious howl"
class SongOfBattle(BaseAbility): key = "song of battle"
class SongOfSummoning(BaseAbility): key = "song of summoning"
class SongOfPower(BaseAbility): key = "song of power"

class ArcFire(BaseAbility):
    key = "arc fire"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost."""
        self.mana_cost = round(6 + self.caster.level * 0.75)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Engulfs the target in an arc of fire."""
        caster = self.caster

        num_dice = 2 + caster.level // 4
        damage = sum(random.randint(1, 12) for _ in range(num_dice))

        caster.msg(f"You engulf {target.key} in an arc of fire!")
        caster.location.msg_contents(
            f"{caster.key} engulfs {target.key} in an arc of fire!",
            exclude=[caster, target]
        )
        target.msg(f"An arc of fire from {caster.key} burns you!")

        # TODO: Implement saving throws.
        target.at_damage(damage, attacker=caster)

class SongOfRejuvenation(BaseAbility): key = "song of rejuvenation"

class ColorSpray(BaseAbility):
    key = "color spray"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost."""
        self.mana_cost = round(5 + self.caster.level * 0.23)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Blasts the target with a spray of colors."""
        caster = self.caster

        num_dice = 2 + caster.level // 10
        damage = sum(random.randint(1, 10) for _ in range(num_dice))

        caster.msg(f"You blast {target.key} with a spray of colors!")
        caster.location.msg_contents(
            f"{caster.key} blasts {target.key} with a spray of colors!",
            exclude=[caster, target]
        )
        target.msg(f"A spray of colors from {caster.key} strikes you!")

        # TODO: Implement saving throws.
        target.at_damage(damage, attacker=caster)

class Warstrike(BaseAbility): key = "warstrike"

class ShockingGrasp(BaseAbility):
    key = "shocking grasp"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost."""
        self.mana_cost = round(6 + self.caster.level * 0.65)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Shocks the target with a touch of electricity."""
        caster = self.caster

        num_dice = 6 + int(caster.level * 3 / 16)
        damage = sum(random.randint(1, 8) for _ in range(num_dice))

        caster.msg(f"You shock {target.key} with a touch of electricity!")
        target.msg(f"{caster.key} shocks you!")

        # TODO: Implement saving throws.
        target.at_damage(damage, attacker=caster)

class Curse(BaseAbility):
    key = "curse"
    mana_cost = 12

    def at_use(self, target, **kwargs):
        """Curses the target, reducing combat effectiveness."""
        caster = self.caster
        # Duration is level minutes. MUD minutes are 60 seconds.
        duration_seconds = caster.level * 60

        debuff_amount = -(caster.level // 20 + 1)

        caster.msg(f"You cast 'curse' on {target.key}.")
        if caster != target:
            target.msg(f"{caster.key} lays a curse upon you!")

        # TODO: Implement saving throws.
        target.buffs.add(
            "curse",
            duration=gametime.gametime(seconds=duration_seconds),
            hitroll=debuff_amount,
            damroll=debuff_amount
        )

class SongOfHaste(BaseAbility): key = "song of haste"

class LightningBolt(BaseAbility):
    key = "lightning bolt"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost."""
        self.mana_cost = round(18 + self.caster.level * 0.125)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Strikes the target with a bolt of lightning."""
        caster = self.caster

        num_dice = 14 + caster.level // 14
        damage = sum(random.randint(1, 8) for _ in range(num_dice)) + 16

        caster.msg(f"A bolt of lightning erupts from your fingertips, striking {target.key}!")
        target.msg(f"{caster.key} strikes you with a lightning bolt!")

        # TODO: Implement saving throws.
        target.at_damage(damage, attacker=caster)

class Sleep(BaseAbility):
    key = "sleep"
    mana_cost = 24

    def check_rules(self, target, **kwargs):
        """Spell fails if target is higher level."""
        if target.level > self.caster.level:
            return (False, "Your target is too powerful to put to sleep.")
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Puts the target to sleep."""
        caster = self.caster
        duration_hours = 1 + caster.level / 6
        duration_seconds = duration_hours * 75

        caster.msg(f"You put {target.key} to sleep.")
        target.msg(f"{caster.key} puts you to sleep!")

        # TODO: Implement saving throws.
        # Using "stun" buff to represent sleep
        target.buffs.add(
            "stun",
            duration=gametime.gametime(seconds=duration_seconds)
        )

class IceStorm(BaseAbility):
    key = "ice storm"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost."""
        self.mana_cost = round(35 + self.caster.level * 0.60)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Pummels the room with a storm of ice."""
        caster = self.caster
        room = caster.location

        num_dice = 6 + caster.level // 8
        damage = sum(random.randint(1, 20) for _ in range(num_dice)) + 20

        caster.msg("You call down a storm of ice!")
        room.msg_contents(
            f"{caster.key} calls down a storm of ice!",
            exclude=[caster]
        )

        for char in room.contents:
            if not char.is_pc and char != caster:
                char.msg("The ice storm pummels you!")
                # TODO: Implement saving throws.
                char.at_damage(damage, attacker=caster)

class SpectreTouch(BaseAbility): key = "spectre touch"
class NecroticStrike(BaseAbility): key = "necrotic strike"
class SongOfRestoration(BaseAbility): key = "song of restoration"
class QuickFix(BaseAbility): key = "quick fix"

class Teleport(BaseAbility):
    key = "teleport"
    mana_cost = 50

    def at_use(self, target, **kwargs):
        """Teleports the caster to a random room."""
        caster = self.caster

        # This will be passed from the command
        stay_in_zone = kwargs.get("zone", False)

        if stay_in_zone:
            # This assumes a "zone" tag on rooms
            possible_destinations = [
                room for room in Room.objects.filter(tags__key="zone", tags__category=caster.location.tags.get("zone", category="zone"))
                if room != caster.location
            ]
        else:
            from evennia.objects.models import ObjectDB
            possible_destinations = [
                room for room in ObjectDB.objects.filter(db_typeclass_path="typeclasses.rooms.Room")
                if room != caster.location
            ]

        if not possible_destinations:
            caster.msg("The teleport fizzles.")
            return

        destination = random.choice(possible_destinations)
        caster.move_to(destination)
        caster.msg("You have been teleported!")

class AcidBreath(BaseAbility):
    key = "acid breath"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost based on targets."""
        room = self.caster.location
        num_targets = len([
            char for char in room.contents
            if not char.is_pc and char != self.caster
        ])

        self.mana_cost = round(1 + (4 + self.caster.level * 0.50) * num_targets)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Breathes acid on all MOBs in the room."""
        caster = self.caster
        room = caster.location

        caster.msg("You breathe a cone of corrosive acid!")
        room.msg_contents(
            f"{caster.key} breathes a cone of corrosive acid!",
            exclude=[caster]
        )

        if caster.vitals.HP.current < 200:
            damage = 100 + random.randint(1, 100)
        else:
            damage = 100 + random.randint(1, caster.vitals.HP.current - 100)

        for char in room.contents:
            # Target all non-player characters
            if not char.is_pc and char != caster:
                char.msg("The acid breath burns you!")
                # TODO: Implement saving throws.
                char.at_damage(damage, attacker=caster)

class FrostBreath(BaseAbility):
    key = "frost breath"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost based on targets."""
        room = self.caster.location
        num_targets = len([
            char for char in room.contents
            if not char.is_pc and char != self.caster
        ])

        self.mana_cost = round(1 + (4 + self.caster.level * 0.50) * num_targets)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Breathes frost on all MOBs in the room."""
        caster = self.caster
        room = caster.location

        if caster.vitals.HP.current < 200:
            damage = 100 + random.randint(1, 100)
        else:
            damage = 100 + random.randint(1, caster.vitals.HP.current - 100)

        caster.msg("You breathe a cone of frost!")
        room.msg_contents(
            f"{caster.key} breathes a cone of frost!",
            exclude=[caster]
        )

        for char in room.contents:
            if not char.is_pc and char != caster:
                char.msg("The frost breath freezes you!")
                # TODO: Implement saving throws.
                char.at_damage(damage, attacker=caster)

class GasBreath(BaseAbility):
    key = "gas breath"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost based on targets."""
        room = self.caster.location
        num_targets = len([
            char for char in room.contents
            if not char.is_pc and char != self.caster
        ])

        self.mana_cost = round(1 + (4 + self.caster.level * 0.50) * num_targets)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Breathes noxious gas on all MOBs in the room."""
        caster = self.caster
        room = caster.location

        if caster.vitals.HP.current < 200:
            damage = 100 + random.randint(1, 100)
        else:
            damage = 100 + random.randint(1, caster.vitals.HP.current - 100)

        caster.msg("You breathe a cloud of noxious gas!")
        room.msg_contents(
            f"{caster.key} breathes a cloud of noxious gas!",
            exclude=[caster]
        )

        for char in room.contents:
            if not char.is_pc and char != caster:
                char.msg("The noxious gas burns your lungs!")
                # TODO: Implement saving throws.
                char.at_damage(damage, attacker=caster)

class FireBreath(BaseAbility):
    key = "fire breath"

    def check_rules(self, target, **kwargs):
        """Check level-based mana cost based on targets."""
        room = self.caster.location
        num_targets = len([
            char for char in room.contents
            if not char.is_pc and char != self.caster
        ])

        self.mana_cost = round(1 + (8 + self.caster.level * 0.50) * num_targets)
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Breathes fire on all MOBs in the room."""
        caster = self.caster
        room = caster.location

        if caster.vitals.HP.current < 200:
            damage = 100 + random.randint(1, 100)
        else:
            damage = 100 + random.randint(1, caster.vitals.HP.current - 100)

        caster.msg("You breathe a cone of fire!")
        room.msg_contents(
            f"{caster.key} breathes a cone of fire!",
            exclude=[caster]
        )

        for char in room.contents:
            if not char.is_pc and char != caster:
                char.msg("The fire breath burns you!")
                # TODO: Implement saving throws.
                char.at_damage(damage, attacker=caster)

class Beacon(BaseAbility): key = "beacon"
class Constitution(BaseAbility): key = "constitution"
class SongOfDevastation(BaseAbility): key = "song of devastation"
class Break(BaseAbility): key = "break"
class Intimidate(BaseAbility): key = "intimidate"
class Malfesor(BaseAbility): key = "malfesor"

class MassInvisibility(BaseAbility):
    key = "mass invisibility"

    def check_rules(self, target, **kwargs):
        """Check mana cost based on group members."""
        caster = self.caster
        if not caster.group.is_in_group:
            return (False, "You are not in a group.")

        num_targets = len(caster.group.group.members)
        self.mana_cost = 21 * num_targets
        return super().check_rules(target, **kwargs)

    def at_use(self, target, **kwargs):
        """Makes all group members invisible."""
        caster = self.caster
        duration_hours = 12 + caster.level / 4
        duration_seconds = duration_hours * 75

        caster.msg("You cast 'mass invisibility'!")

        for member in caster.group.group.members:
            member.msg("You fade from sight.")
            member.buffs.add(
                "invisibility",
                duration=gametime.gametime(seconds=duration_seconds),
                ac=40
            )

class Bloodlust(BaseAbility):
    key = "bloodlust"
    mana_cost = 20

    def at_use(self, target, **kwargs):
        """Increases the target's core stats."""
        caster = self.caster
        # 6 MUD hours * 75 seconds/hour
        duration_seconds = 6 * 75

        caster.msg(f"You cast 'bloodlust' on {target.key}.")
        if caster != target:
            target.msg(f"{caster.key} fills you with a lust for blood!")

        target.buffs.add(
            "bloodlust",
            duration=gametime.gametime(seconds=duration_seconds),
            INT=10,
            CON=10,
            STR=10
        )

class Lifebreaker(BaseAbility): key = "lifebreaker"
class Souldrinker(BaseAbility): key = "souldrinker"
class Headbang(BaseAbility): key = "headbang"
class UnholyFist(BaseAbility): key = "unholy fist"

class Archery(BaseAbility):
    key = "archery"

    def at_use(self, target, **kwargs):
        """Grants the ability to use ranged weapons."""
        caster = self.caster
        caster.msg("You have learned the ways of the bow.")
        caster.buffs.add("archery", duration=-1)

class PointBlankShot(BaseAbility): key = "point-blank shot"
class ConcussiveShot(BaseAbility): key = "concussive shot"

class Barrage(BaseAbility):
    key = "barrage"
    mana_cost = 50 # Represents movement points

    def at_use(self, target, **kwargs):
        """A melee area-of-effect attack."""
        caster = self.caster
        room = caster.location

        dex_mod = (caster.stats.DEX.value - 10) // 2
        damage = dex_mod + caster.vitals.MP.current // 10

        caster.msg("You unleash a barrage of attacks!")

        for char in room.contents:
            if not char.is_pc and char != caster:
                char.msg("You are caught in the barrage!")
                char.at_damage(damage, attacker=caster)

class PiercingShot(BaseAbility): key = "piercing shot"
class Wildfire(BaseAbility): key = "wildfire"
class MindJab(BaseAbility): key = "mind jab"
class MindBlade(BaseAbility): key = "mind blade"
class ToxicCloud(BaseAbility): key = "toxic cloud"
class DeathStrike(BaseAbility): key = "death strike"
class Restoration(BaseAbility): key = "restoration"

class HolyWordRestore(BaseAbility):
    key = "holy word restore"
    cooldown = 480 * 48 # 480 seconds * 48

    def at_use(self, target, **kwargs):
        """Fully restores the caster's health."""
        caster = self.caster

        caster.vitals.HP.current = caster.vitals.HP.max
        caster.msg("|gA holy word restores you to full health!|n")

class Purify(BaseAbility): key = "purify"
class HolyWordReckoning(BaseAbility): key = "holy word reckoning"
class GuardianAngel(BaseAbility): key = "guardian angel"
class Platebreaker(BaseAbility): key = "platebreaker"
class Whirlwind(BaseAbility): key = "whirlwind"
class MortalStrike(BaseAbility): key = "mortal strike"
class DefensiveStance(BaseAbility): key = "defensive stance"
class Rage(BaseAbility): key = "rage"
class PowerWordParalyze(BaseAbility): key = "power word paralyze"
class Maelstrom(BaseAbility): key = "maelstrom"
class LimitedInvulnerabil(BaseAbility): key = "limited invulnerabil"
class PowerWordBlind(BaseAbility): key = "power word blind"
class GravityFocus(BaseAbility): key = "gravity focus"
class Wish(BaseAbility): key = "wish"
class TensersTransformati(BaseAbility): key = "tensers transformati"
class PowerWordKill(BaseAbility): key = "power word kill"
class Invulnerability(BaseAbility): key = "invulnerability"
class Familiar(BaseAbility): key = "familiar"
class PestilentialBlast(BaseAbility): key = "pestilential blast"
class RaiseSkeleton(BaseAbility): key = "raise skeleton"
class RaiseZombie(BaseAbility): key = "raise zombie"
class RaiseMage(BaseAbility): key = "raise mage"
class SoulCoil(BaseAbility): key = "soul coil"
class DeathTouch(BaseAbility): key = "death touch"
class DeathCoil(BaseAbility): key = "death coil"
class RaiseVampire(BaseAbility): key = "raise vampire"
class RaiseDead(BaseAbility): key = "raise dead"
class RaiseDracolich(BaseAbility): key = "raise dracolich"
class MotleyCrew(BaseAbility): key = "motley crew"
class Chokehold(BaseAbility): key = "chokehold"
class DoubleCross(BaseAbility): key = "double cross"
class Thrust(BaseAbility): key = "thrust"
