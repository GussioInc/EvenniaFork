# mygame/world/groups.py

class Group:
    """
    Represents a group of characters.
    """
    def __init__(self, leader):
        self.leader = leader
        self.members = {leader}

    def add_member(self, character):
        """Adds a character to the group."""
        self.members.add(character)
        character.group.group = self

    def remove_member(self, character):
        """Removes a character from the group."""
        if character in self.members:
            self.members.remove(character)
            character.group.group = None
            if not self.members or character == self.leader:
                self.disband()

    def disband(self):
        """Disbands the entire group."""
        for member in list(self.members):
            member.group.group = None
        self.members.clear()
        self.leader = None

    def send_message(self, message):
        """Sends a message to all group members."""
        for member in self.members:
            member.msg(message)
