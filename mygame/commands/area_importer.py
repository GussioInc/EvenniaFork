# mygame/commands/area_importer.py

from evennia import Command
from evennia.utils import create
from world.area_parser import DikuAreaParser

class CmdImportArea(Command):
    """
    Imports a DikuMUD .are file.

    Usage:
      +importarea <file_path>
    """
    key = "+importarea"
    help_category = "admin"
    locks = "perm(Admin)"

    def func(self):
        """Implements the command."""
        if not self.args:
            self.msg("Usage: +importarea <file_path>")
            return

        file_path = self.args.strip()
        parser = DikuAreaParser()

        try:
            parsed_data = parser.parse(file_path)
            self.msg(f"Successfully parsed {file_path}.")

            rooms = self._create_rooms(parsed_data["rooms"])
            mobiles = self._create_mobiles(parsed_data["mobiles"])
            objects = self._create_objects(parsed_data["objects"])

            self._handle_resets(parsed_data["resets"], rooms, mobiles, objects)

            self.msg("Area import complete.")

        except FileNotFoundError:
            self.msg(f"File not found: {file_path}")
        except Exception as e:
            self.msg(f"An error occurred: {e}")

    def _create_rooms(self, room_data):
        """Creates room objects from parsed data."""
        rooms = {}
        for vnum, data in room_data.items():
            room = create.create_object("typeclasses.rooms.Room", key=data["name"], attributes={"desc": data["desc"]})
            room.db.vnum = vnum
            rooms[vnum] = room
        self.msg(f"Created {len(rooms)} rooms.")
        return rooms

    def _create_mobiles(self, mobile_data):
        """Creates mobile character objects from parsed data."""
        mobiles = {}
        for vnum, data in mobile_data.items():
            mob = create.create_object("typeclasses.characters.Character", key=data["short_desc"], attributes={"desc": data["long_desc"]})
            mob.db.vnum = vnum
            mobiles[vnum] = mob
        self.msg(f"Created {len(mobiles)} mobiles.")
        return mobiles

    def _create_objects(self, object_data):
        """Creates object instances from parsed data."""
        objects = {}
        for vnum, data in object_data.items():
            obj = create.create_object("typeclasses.objects.Object", key=data["short_desc"], attributes={"desc": data["long_desc"]})
            obj.db.vnum = vnum
            objects[vnum] = obj
        self.msg(f"Created {len(objects)} objects.")
        return objects

    def _handle_resets(self, reset_data, rooms, mobiles, objects):
        """Handles the reset data to place mobs and objects."""
        for reset_line in reset_data:
            parts = reset_line.split()
            command = parts[0]
            if command == "M":  # Mobile reset
                mob_vnum = int(parts[2])
                room_vnum = int(parts[4])
                if mob_vnum in mobiles and room_vnum in rooms:
                    mobiles[mob_vnum].location = rooms[room_vnum]
            elif command == "O":  # Object reset
                obj_vnum = int(parts[2])
                room_vnum = int(parts[4])
                if obj_vnum in objects and room_vnum in rooms:
                    objects[obj_vnum].location = rooms[room_vnum]
            elif command == "G":  # Give object to mobile
                obj_vnum = int(parts[2])
                # Find the last loaded mobile
                last_mob = None
                for mob in mobiles.values():
                    if mob.location:
                        last_mob = mob
                if obj_vnum in objects and last_mob:
                    objects[obj_vnum].location = last_mob
            elif command == "E":  # Equip object on mobile
                obj_vnum = int(parts[2])
                # Find the last loaded mobile
                last_mob = None
                for mob in mobiles.values():
                    if mob.location:
                        last_mob = mob
                if obj_vnum in objects and last_mob:
                    objects[obj_vnum].location = last_mob
                    # Don't have a way to equip yet, so just put in inventory
        self.msg("Processed resets.")
