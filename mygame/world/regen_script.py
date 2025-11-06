# mygame/world/regen_script.py
from evennia.scripts.scripts import DefaultScript

class RegenScript(DefaultScript):
    """
    A simple script attached to all living characters
    to handle baseline HP/MP regeneration.
    """
    def at_script_creation(self):
        self.key = "RegenScript"
        self.desc = "Handles HP/MP regeneration."
        self.interval = 60  # Ticks once per minute
        self.persistent = True
        self.repeats = 0  # Infinite
        self.db.last_tick = 0

    def at_repeat(self):
        """Called every 'interval' seconds."""
        if not self.obj:
            return  # Failsafe

        # Don't regen if in combat
        if self.obj.combat.is_in_combat():
            return

        # Use the VitalsHandler to heal
        # 'current' is a property on the GaugeTrait that handles clamping
        hp_regen = self.obj.stats.CON.value // 2  # Example formula
        mp_regen = self.obj.stats.INT.value // 2  # Example formula
        
        self.obj.vitals.HP.current += hp_regen
        self.obj.vitals.MP.current += mp_regen
        
        #
        # handle spell maintenance
        #
        
        if self.db.last_tick % 3600 == 0:
            for buff in self.obj.buffs.all:
                if buff.maintenance_cost > 0:
                    if self.obj.vitals.MP.current >= buff.maintenance_cost:
                        self.obj.vitals.MP.current -= buff.maintenance_cost
                    else:
                        self.obj.buffs.remove(buff.key)
                        self.obj.msg(f"You don't have enough mana to maintain {buff.key}, and it fades.")
        
        self.db.last_tick += self.interval
