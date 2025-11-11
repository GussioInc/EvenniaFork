# mygame/commands/equipment_commands.py

from evennia.contrib.rpg.equipment import CmdWear as ContribCmdWear

class CmdWear(ContribCmdWear):
    """
    Custom wear command to enforce class armor restrictions.
    """
    def func(self):
        """Implement the wear command."""
        caller = self.caller

        if not self.args:
            caller.msg("Usage: wear <obj>")
            return

        obj_to_wear = caller.search(self.args)
        if not obj_to_wear:
            return

        # --- Armor Restriction Check ---
        armor_type = obj_to_wear.db.armor_type
        if armor_type and armor_type > caller.class_handler.get_class_obj().armor_restriction:
            caller.msg("Your class cannot wear that type of armor.")
            return

        # If the check passes, call the original func
        super().func()
