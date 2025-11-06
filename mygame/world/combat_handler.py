# mygame/world/combat_handler.py
from evennia.scripts.scripts import DefaultScript
from evennia.utils import logger
import random

class CombatHandler(DefaultScript):
    """
    Manages a single combat encounter in a room.
    Replaces violence_update.
    """
    
    def at_script_creation(self):
        self.key = "CombatHandler"
        self.interval = 2  # Diku-style 2-second combat round
        self.persistent = True
        self.repeats = 0 # Runs until manually stopped
        
        # This list holds all participants
        self.db.combatants = []
        # This dict tracks NPC aggro: {npc: {pc: hate_value,...},...}
        self.db.aggro_map = {}

    def add_combatant(self, combatant):
        """Adds a new combatant to the fight."""
        if combatant not in self.db.combatants:
            self.db.combatants.append(combatant)
            combatant.combat.join_combat(self)
            
    def remove_combatant(self, combatant):
        """Removes a combatant from the fight (fled, died)."""
        if combatant in self.db.combatants:
            self.db.combatants.remove(combatant)
            combatant.combat.leave_combat()
            
            # Clear this combatant's aggro
            if combatant in self.db.aggro_map:
                del self.db.aggro_map[combatant]
            for npc, hate_list in self.db.aggro_map.items():
                if combatant in hate_list:
                    del hate_list[combatant]
        
        if self.check_combat_end():
            self.stop() # Stops the script's timer

    def at_stop(self):
        """Called when script is stopped. Cleans up all combatants."""
        for char in self.db.combatants:
            char.combat.leave_combat()
        self.db.combatants = []
        self.db.aggro_map = {}

    def check_combat_end(self):
        """Checks if combat should end."""
        pcs = [c for c in self.db.combatants if c.is_pc]
        npcs = [c for c in self.db.combatants if not c.is_pc]
        return not pcs or not npcs

    def add_aggro(self, npc, target, amount):
        """Adds 'amount' of hate for 'target' to 'npc's list."""
        if npc not in self.db.aggro_map:
            self.db.aggro_map[npc] = {}
        
        if target not in self.db.aggro_map[npc]:
            self.db.aggro_map[npc][target] = 0
            
        self.db.aggro_map[npc][target] += amount

    # This is the new "violence_update"
    def at_repeat(self):
        """
        The main combat loop. Called every 'interval' seconds.
        """
        if not self.db.combatants:
            self.stop()
            return
            
        # Create a copy to avoid mutation issues during the loop
        for combatant in list(self.db.combatants):
            if combatant.vitals.HP.current <= 0:
                continue
                
            # Get this combatant's intended target
            target = combatant.combat.target
            
            # --- NPC AI / Aggro Logic ---
            if not combatant.is_pc:
                target = self.get_npc_target(combatant)
                if not target:
                    continue # No one to fight
                combatant.combat.target = target # Set intent

            # --- Target Validation ---
            if not target or target not in self.db.combatants or \
               target.vitals.HP.current <= 0:
                combatant.combat.target = None
                # PC finds a new target
                if combatant.is_pc:
                    # Diku-style: auto-attack next available enemy
                    new_target = self.find_next_target(combatant)
                    combatant.combat.target = new_target
                continue
                
            # --- Resolution ---
            self.resolve_attack(combatant, target)

    def get_npc_target(self, npc):
        """Finds a target for an NPC based on the aggro map."""
        hate_list = self.db.aggro_map.get(npc, {})
        if not hate_list:
            # No hate, find a random PC target
            return self.find_next_target(npc)

        # Find the target with the highest hate value
        return max(hate_list, key=hate_list.get)
        
    def find_next_target(self, attacker):
        """Finds any valid target in the room."""
        is_pc = attacker.is_pc
        for target in self.db.combatants:
            if target.is_pc!= is_pc and target.vitals.HP.current > 0:
                return target
        return None

    def resolve_attack(self, attacker, defender):
        """
        Calculates and applies a single attack.
        This is where D&D hit/damage formulas are ported.
        """
        # 1. Hit Roll
        # Get modifier from StatsHandler, including buffs
        str_mod = (attacker.stats.STR.value - 10) // 2
        # Get "to_hit" bonus from buffs (e.g., "Bless" spell)
        hit_bonus = attacker.buffs.get_mod("to_hit") # (Part IV)
        
        # Assumes defender has an @property 'ac' for Armor Class
        hit_roll = random.randint(1, 20)
        
        if hit_roll + str_mod + hit_bonus < defender.buffs.get_mod("armor"):
            attacker.msg(f"You miss {defender.key}!")
            defender.msg(f"{attacker.key} misses you!")
            return

        # 2. Damage Roll
        # Example: 1d8 (weapon) + STR mod
        dmg = random.randint(1, 8) + str_mod
        
        # 3. Apply Damage
        # at_damage will handle aggro generation
        defender.at_damage(dmg, attacker)
        
        attacker.msg(f"You hit {defender.key} for {dmg} damage!")
        defender.msg(f"{attacker.key} hits you for {dmg} damage!")
        # mygame/world/combat_handler.py

class CharacterCombatHandler:
    """
    A non-persistent helper class attached to Characters
    to store their individual combat state.
    """
    def __init__(self, obj):
        self.obj = obj
        self.initialize()
        
    def initialize(self):
        # self.handler is a back-reference to the main room handler
        self.handler = None
        self.target = None # Who this char is trying to hit

    @property
    def is_in_combat(self):
        return bool(self.handler)
        
    def join_combat(self, handler):
        self.handler = handler
        self.obj.msg("You have joined the fight!")
        
    def leave_combat(self):
        self.handler = None
        self.target = None
        self.obj.msg("You are no longer in combat.")
