# mygame/world/convert_area.py

import sys
from area_parser import DikuAreaParser

def convert_area(input_path, output_path):
    """
    Converts a DikuMUD .are file to an Evennia batch build file.
    """
    parser = DikuAreaParser()
    parsed_data = parser.parse(input_path)

    with open(output_path, 'w') as f:
        f.write("# Evennia batch build file for New Thalos\n\n")

        # Create rooms
        f.write("# Rooms\n")
        for vnum, room_data in parsed_data["rooms"].items():
            f.write(f'ev.create_object("typeclasses.rooms.Room", key="{room_data["name"]}", attributes=[("desc", """{room_data["desc"]}"""), ("vnum", {vnum})])\n')

        # Create mobiles
        f.write("\n# Mobiles\n")
        for vnum, mob_data in parsed_data["mobiles"].items():
            f.write(f'ev.create_object("typeclasses.characters.Character", key="{mob_data["short_desc"]}", attributes=[("desc", """{mob_data["long_desc"]}"""), ("vnum", {vnum})])\n')

        # Create objects
        f.write("\n# Objects\n")
        for vnum, obj_data in parsed_data["objects"].items():
            f.write(f'ev.create_object("typeclasses.objects.Object", key="{obj_data["short_desc"]}", attributes=[("desc", """{obj_data["long_desc"]}"""), ("vnum", {vnum})])\n')

        # Handle resets
        f.write("\n# Resets\n")
        for reset_line in parsed_data["resets"]:
            parts = reset_line.split()
            command = parts[0]
            if command == "M":
                mob_vnum = int(parts[2])
                room_vnum = int(parts[4])
                f.write(f'ev.search_object("vnum", {mob_vnum})[0].location = ev.search_object("vnum", {room_vnum})[0]\n')
            elif command == "O":
                obj_vnum = int(parts[2])
                room_vnum = int(parts[4])
                f.write(f'ev.search_object("vnum", {obj_vnum})[0].location = ev.search_object("vnum", {room_vnum})[0]\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_area.py <input_path> <output_path>")
    else:
        convert_area(sys.argv[1], sys.argv[2])
        print(f"Converted {sys.argv[1]} to {sys.argv[2]}")
