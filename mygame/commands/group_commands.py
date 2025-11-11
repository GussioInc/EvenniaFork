# mygame/commands/group_commands.py

from evennia import Command

class CmdFollow(Command):
    """
    Follow another character.

    Usage:
      follow <character>
      follow self
      unfollow
    """
    key = "follow"
    aliases = ["unfollow"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """Implements the follow command."""
        caller = self.caller
        args = self.args.strip()

        if not args or args.lower() in ["self", "me"]:
            if not caller.ndb.follow_target:
                caller.msg("You aren't following anyone.")
                return

            target = caller.ndb.follow_target
            caller.msg(f"You stop following {target.key}.")
            target.msg(f"{caller.key} stops following you.")
            caller.ndb.follow_target = None
            return

        target = caller.search(args)
        if not target:
            return

        if target == caller:
            caller.msg("You can't follow yourself.")
            return

        caller.ndb.follow_target = target
        caller.msg(f"You start following {target.key}.")
        target.msg(f"{caller.key} starts following you.")

class CmdGroup(Command):
    """
    Manage your group.

    Usage:
      group <character>
      group all
      ungroup <character>
      ungroup all
    """
    key = "group"
    aliases = ["ungroup"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """Implements the group command."""
        caller = self.caller
        args = self.args.strip().lower()

        # --- Ungrouping Logic ---
        if self.cmdstring == "ungroup":
            if not caller.group.is_in_group:
                caller.msg("You are not in a group.")
                return
            if not caller.group.is_leader:
                caller.msg("You are not the leader of this group.")
                return

            if args == "all":
                caller.group.group.send_message(f"{caller.key} disbands the group.")
                caller.group.group.disband()
            else:
                target = caller.search(args)
                if not target:
                    return
                if target not in caller.group.group.members:
                    caller.msg(f"{target.key} is not in your group.")
                    return

                caller.group.group.remove_member(target)
                caller.group.group.send_message(f"{caller.key} removes {target.key} from the group.")
                target.msg(f"You have been removed from the group by {caller.key}.")

            return

        # --- Grouping Logic ---
        if not args:
            caller.msg("Usage: group <character> or group all")
            return

        followers = [
            char for char in caller.location.contents
            if hasattr(char, "ndb") and char.ndb.follow_target == caller
        ]

        if not followers:
            caller.msg("No one is following you.")
            return

        # Create a new group if the caller isn't in one
        if not caller.group.is_in_group:
            from world.groups import Group
            caller.group.group = Group(caller)
            caller.msg("You form a new group.")

        if not caller.group.is_leader:
            caller.msg("You cannot add members to a group you don't lead.")
            return

        targets = []
        if args == "all":
            targets = followers
        else:
            target = caller.search(args)
            if not target:
                return
            if target not in followers:
                caller.msg(f"{target.key} is not following you.")
                return
            targets.append(target)

        for target in targets:
            if not target.group.is_in_group:
                caller.group.group.add_member(target)
                caller.group.group.send_message(f"{target.key} has joined the group.")
            else:
                caller.msg(f"{target.key} is already in a group.")

class CmdGTell(Command):
    """
    Send a message to your group.

    Usage:
      gtell <message>
      gt <message>
    """
    key = "gtell"
    aliases = ["gt"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """Implements the gtell command."""
        caller = self.caller
        args = self.args.strip()

        if not caller.group.is_in_group:
            caller.msg("You are not in a group.")
            return

        if not args:
            caller.msg("Usage: gtell <message>")
            return

        message = f"|c[Group]|n {caller.key}: {args}"
        caller.group.group.send_message(message)

class CmdGWho(Command):
    """
    Shows information about your group.

    Usage:
      gwho
    """
    key = "gwho"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """Implements the gwho command."""
        caller = self.caller

        if not caller.group.is_in_group:
            caller.msg("You are not in a group.")
            return

        group = caller.group.group
        leader = group.leader
        members = group.members

        table = self.styled_table(
            "|wGroup Leader",
            "|wMember",
            "|wHP",
            "|wMP",
            "|wLocation",
            "|wXP Share"
        )

        xp_share = 100 // len(members)

        for member in members:
            is_leader_str = " (L)" if member == leader else ""
            hp_str = f"{member.vitals.HP.current}/{member.vitals.HP.max}"
            mp_str = f"{member.vitals.MP.current}/{member.vitals.MP.max}"

            table.add_row(
                leader.key if member == leader else "",
                member.key + is_leader_str,
                hp_str,
                mp_str,
                member.location.key,
                f"{xp_share}%"
            )

        caller.msg(f"|c--- Group: {leader.key}'s Party ---|n")
        caller.msg(str(table))
