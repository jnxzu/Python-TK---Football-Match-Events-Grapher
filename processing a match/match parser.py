import json


class Event:
    def __init__(self, period, e_min, e_type, player, team, location, outcome):
        if period == 1 and e_min > 45:
            e_min = 45  # ADDITIONAL TIME (1ST HALF) COUNTED AS 45TH MINUTE
        elif period == 2 and e_min > 90:
            e_min = 90  # ADDITIONAL TIME (2ND HALF) COUNTED AS 90TH MINUTE
        else:
            self.min = e_min
        self.type = e_type
        self.player = player
        self.team = team
        self.location = location
        self.outcome = outcome


class Dribble(Event):
    def __init__(self, period, e_min, e_type, player, team, location, outcome):
        super().__init__(period, e_min, "Dribble", player, team, location, outcome)


class Tackle(Event):
    def __init__(self, period, e_min, e_type, player, team, location, outcome):
        super().__init__(period, e_min, "Tackle", player, team, location, outcome)


class Interception(Event):
    def __init__(self, period, e_min, e_type, player, team, location, outcome):
        super().__init__(period, e_min, "Interception", player, team, location, outcome)


class Pass(Event):
    def __init__(self, period, e_min, e_type, player, team, location, outcome, destination, assist=False):
        super().__init__(period, e_min, "Pass", player, team, location, outcome)
        self.destination = destination
        self.assist = assist


class Shot(Event):
    def __init__(self, period, e_min, e_type, player, team, location, outcome, destination, goal=False):
        super().__init__(period, e_min, "Shot", player, team, location, outcome)
        self.destination = destination
        self.goal = goal


with open("processing a match/15946.json") as f:
    data = json.load(f)
    match = ()
    players = {}
    events = []
    for event in data:

        period = event["period"]  # PERIOD OF THE GAME (1/2 HALF)
        if period > 2:
            break  # NO SUPPORT FOR EXTRA TIME/PENALTIES
        minute = event["minute"]  # MINUTE OF THE MATCH

        e_type = event["type"]["id"]  # EVENT TYPE
        if e_type not in [14, 4, 21, 10, 30, 16, 19]:
            # IGNORE UNSUPPORTED EVENTS (PREVENTS ISSUES WITH FOLLOWING FIELDS NOT BEING PRESENT)
            continue

        player = (event["player"]["id"], event["player"]
                  ["name"])  # PLAYER ID AND NAME
        team = (event["team"]["id"], event["team"]["name"])  # TEAM ID AND NAME
        location = event["location"]  # LOCATION [X,Y]

        if e_type == 14:  # DRIBBLE
            outcome = event["dribble"]["outcome"]["id"]
            if outcome == 8:  # IF DRIBBLE COMPLETE (ID 8) OR INCOMPLETE (ID 9)
                outcome = 1  # COMPLETE
            else:
                outcome = 0  # INCOMPLETE

        elif e_type == 4 or e_type == 21:  # DUEL OR FOUL COMMITED
            pass
            # TODO
        elif e_type == 10:  # INTERCEPTION
            pass
            # TODO
        elif e_type == 30:  # PASS
            pass
            # TODO
        elif e_type == 16:  # SHOT
            pass
            # TODO
        elif e_type == 19:  # SUBSTITUTION
            pass
            # TODO

    match.append(players)
    match.append(events)
