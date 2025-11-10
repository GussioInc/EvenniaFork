# mygame/commands/combat_commands.py
from evennia import Command, scripts

class CmdKill(Command):
    """
    Initiates combat with a target.
    
    Usage:
      kill <target>
    """
    key = "kill"
    aliases = ["attack"]
    
    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Who do you want to attack?")
            return
            
        target = caller.search(self.args.strip())
        if not target:
            return # search() handles error message
            
        # Find or create the room's CombatHandler
        try:
            handler = caller.location.scripts.get("CombatHandler")
        except IndexError:
            handler = caller.location.scripts.add(
                "world.combat_handler.CombatHandler"
            )
            
        # Add combatants and set intent
        handler.add_combatant(caller)
        handler.add_combatant(target)
        caller.combat.target = target
        
        # Add initial aggro to start the fight
        if not target.is_pc:
            handler.add_aggro(target, caller, 1)

class CmdUse(Command):
    """
    Casts a spell or uses a skill.
    
    Usage:
      use <skill> [on <target>]
      cast <skill> [on <target>]
    """
    key = "use"
    aliases = ["cast"]
    
    def parse(self):
        """Parses 'skill on target' syntax"""
        args = self.args.strip()
        self.skill_key = ""
        self.target_name = ""
        
        if " on " in args:
            self.skill_key, self.target_name = [
                part.strip() for part in args.split(" on ", 1)
            ]
        else:
            self.skill_key = args
            # If no target, try to use combat target
            self.target_name = self.caller.combat.target
            
    def func(self):
        """Delegate all logic to the handler"""
        if not self.skill_key:
            self.caller.msg("Cast what?")
            return
            
        target = self.caller.search(self.target_name)
        if not target:
            return
            
        # Delegate!
        self.caller.skills.execute(self.skill_key, target=target)

class CmdWeather(Command):
    """
    Check the current weather.

    Usage:
      weather
    """
    key = "weather"
    help_category = "General"

    def func(self):
        """Implements the command."""
        weather_script = scripts.get_script("weather_script")
        if weather_script:
            weather_desc = weather_script.get_weather_desc()
            self.caller.msg(f"You check the skies. {weather_desc}")
        else:
            self.caller.msg("The weather seems to be offline.")


class CmdDispel(Command):
    """
    Dispels a magical effect from a target.
    
    Usage:
      dispel <buff> on <target>
    """
    key = "dispel"
    
    def parse(self):
        """Parses '<buff> on <target>' syntax"""
        args = self.args.strip()
        self.buff_key = ""
        self.target_name = ""
        
        if " on " in args:
            self.buff_key, self.target_name = [
                part.strip() for part in args.split(" on ", 1)
            ]
        else:
            self.caller.msg("Usage: dispel <buff> on <target>")
            
    def func(self):
        """Delegate all logic to the handler"""
        if not self.buff_key:
            return
            
        target = self.caller.search(self.target_name)
        if not target:
            return
            
        if target.buffs.has(self.buff_key):
            target.buffs.remove(self.buff_key)
            self.caller.msg(f"You have dispelled {self.buff_key} from {target.key}.")
            if self.caller != target:
                target.msg(f"{self.caller.key} has dispelled {self.buff_key} from you.")
        else:
            self.caller.msg(f"{target.key} does not have the {self.buff_key} buff.")