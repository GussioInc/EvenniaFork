# mygame/world/area_parser.py

class DikuAreaParser:
    """
    A parser for DikuMUD-style .are files.
    """
    def __init__(self):
        self.area_data = {}
        self.mobiles = {}
        self.objects = {}
        self.rooms = {}
        self.resets = []
        self.shops = []
        self.specials = []

    def parse(self, file_path):
        """
        Parses the entire .are file.
        """
        with open(file_path, 'r') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("#AREADATA"):
                i = self._parse_areadata(lines, i)
            elif line.startswith("#MOBILES"):
                i = self._parse_mobiles(lines, i)
            elif line.startswith("#OBJECTS"):
                i = self._parse_objects(lines, i)
            elif line.startswith("#ROOMS"):
                i = self._parse_rooms(lines, i)
            elif line.startswith("#RESETS"):
                i = self._parse_resets(lines, i)
            elif line.startswith("#SHOPS"):
                i = self._parse_shops(lines, i)
            elif line.startswith("#SPECIALS"):
                i = self._parse_specials(lines, i)
            else:
                i += 1

        return {
            "areadata": self.area_data,
            "mobiles": self.mobiles,
            "objects": self.objects,
            "rooms": self.rooms,
            "resets": self.resets,
            "shops": self.shops,
            "specials": self.specials,
        }

    def _parse_areadata(self, lines, i):
        """Parses the #AREADATA section."""
        # Placeholder
        return i + 1

    def _parse_mobiles(self, lines, i):
        """Parses the #MOBILES section."""
        i += 1
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("#0"):
                return i + 1
            if line.startswith("#"):
                vnum = int(line[1:])
                mobile_data = {
                    "vnum": vnum,
                    "keywords": self._read_tilde_string(lines, i+1),
                    "short_desc": self._read_tilde_string(lines, i+2),
                    "long_desc": self._read_tilde_string(lines, i+3),
                    "full_desc": self._read_tilde_string(lines, i+4),
                }
                i += 5
                # Skip the rest of the mobile data for now
                while i < len(lines) and not lines[i].strip().startswith("#"):
                    i += 1
                self.mobiles[vnum] = mobile_data
            else:
                i += 1
        return i

    def _parse_objects(self, lines, i):
        """Parses the #OBJECTS section."""
        i += 1
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("#0"):
                return i + 1
            if line.startswith("#"):
                vnum = int(line[1:])
                object_data = {
                    "vnum": vnum,
                    "keywords": self._read_tilde_string(lines, i+1),
                    "short_desc": self._read_tilde_string(lines, i+2),
                    "long_desc": self._read_tilde_string(lines, i+3),
                }
                i += 4
                # Skip the rest of the object data for now
                while i < len(lines) and not lines[i].strip().startswith("#"):
                    i += 1
                self.objects[vnum] = object_data
            else:
                i += 1
        return i

    def _parse_rooms(self, lines, i):
        """Parses the #ROOMS section."""
        i += 1
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("#0"):
                return i + 1
            if line.startswith("#"):
                vnum = int(line[1:])
                room_data = {
                    "vnum": vnum,
                    "name": self._read_tilde_string(lines, i+1),
                    "desc": self._read_tilde_string(lines, i+2),
                    "exits": {},
                }
                i += 3
                while i < len(lines) and lines[i].strip() != "S":
                    line = lines[i].strip()
                    if line.startswith("D"):
                        try:
                            parts = line.split()
                            if len(parts) < 4:
                                i += 1
                                continue
                            direction = int(parts[0][1:])
                            exit_data = {
                                "desc": self._read_tilde_string(lines, i+1),
                                "keywords": self._read_tilde_string(lines, i+2),
                                "locks": int(parts[1]),
                                "key": int(parts[2]),
                                "to_vnum": int(parts[3]),
                            }
                            room_data["exits"][direction] = exit_data
                            i += 3
                        except (ValueError, IndexError):
                            # Skip malformed exit lines
                            i += 1
                            continue
                    else:
                        i += 1
                self.rooms[vnum] = room_data
            else:
                i += 1
        return i

    def _read_tilde_string(self, lines, i):
        """Reads a tilde-terminated string from the lines."""
        string = ""
        while i < len(lines):
            line = lines[i]
            if "~" in line:
                string += line.split("~")[0]
                return string.strip()
            else:
                string += line
            i += 1
        return string.strip()

    def _parse_resets(self, lines, i):
        """Parses the #RESETS section."""
        i += 1
        while i < len(lines):
            line = lines[i].strip()
            if line == "S":
                return i + 1
            if line:
                self.resets.append(line)
            i += 1
        return i

    def _parse_shops(self, lines, i):
        """Parses the #SHOPS section."""
        # Placeholder
        return i + 1

    def _parse_specials(self, lines, i):
        """Parses the #SPECIALS section."""
        # Placeholder
        return i + 1
