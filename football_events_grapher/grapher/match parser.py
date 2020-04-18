import json


class Match:
    def __init__(self):
        self.teams = []
        self.starters = []
        self.subs = []


class Player:
    def __init__(self, id, name, team, pos, num):
        self.id = id
        self.name = name
        self.team = team
        self.pos = pos
        self.num = num
        self.events = []


class Event:
    def __init__(self, period, minute, event_type, player, team, location, outcome):
        if period == 1 and minute > 45:
            minute = 45  # ADDITIONAL TIME (1ST HALF) COUNTED AS 45TH MINUTE
        elif period == 2 and minute > 90:
            minute = 90  # ADDITIONAL TIME (2ND HALF) COUNTED AS 90TH MINUTE
        else:
            self.min = minute
        self.type = event_type
        self.player = player
        self.team = team
        self.location = location
        self.outcome = outcome


class Dribble(Event):
    def __init__(self, period, minute, player, team, location, outcome):
        super().__init__(period, minute, "Dribble", player, team, location, outcome)


class Tackle(Event):
    def __init__(self, period, minute, player, team, location, outcome):
        super().__init__(period, minute, "Tackle", player, team, location, outcome)


class Interception(Event):
    def __init__(self, period, minute, player, team, location, outcome):
        super().__init__(period, minute, "Interception", player, team, location, outcome)


class Pass(Event):
    def __init__(self, period, minute, player, team, location, outcome, destination, assist=False):
        super().__init__(period, minute, "Pass", player, team, location, outcome)
        self.destination = destination
        self.assist = assist


class Shot(Event):
    def __init__(self, period, minute, player, team, location, outcome, destination, goal=False):
        super().__init__(period, minute, "Shot", player, team, location, outcome)
        self.destination = destination
        self.goal = goal


def parseMatch(file):
    with open(file) as f:
        data = json.load(f)
        match = Match()
        for d in data[:2]:
            match.teams.append(d['team'])
            for p in d['tactics']['lineup']:
                new_player = Player(p['player']['id'], p['player']
                                    ['name'], p['position']['name'], d['team']['id'], p['jersey_number'])
                match.starters.append(new_player)
        for event in data[2:]:

            period = event["period"]  # PERIOD OF THE GAME (1/2 HALF)
            if period > 2:
                break  # NO SUPPORT FOR EXTRA TIME/PENALTIES
            minute = event["minute"]  # MINUTE OF THE MATCH

            event_type = event["type"]["id"]  # EVENT TYPE
            if event_type not in [14, 4, 21, 10, 30, 16, 19]:
                # IGNORE UNSUPPORTED EVENTS (PREVENTS ISSUES WITH FOLLOWING FIELDS NOT BEING PRESENT)
                continue

            player = event["player"]["id"]  # PLAYER ID
            team = event["team"]["id"]  # TEAM ID
            if event_type != 19:
                location = event["location"]  # LOCATION [X,Y]

            if event_type == 14:  # DRIBBLE
                outcome = event["dribble"]["outcome"]["id"]
                # IF DRIBBLE COMPLETE (ID 8) OR INCOMPLETE (ID 9)
                if outcome == 8:
                    outcome = True  # COMPLETE
                else:
                    outcome = False  # INCOMPLETE
                new_event = Dribble(period, minute, player,
                                    team, location, outcome)
                for p in match.starters+match.subs:
                    if p.id == player:
                        p.events.append(new_event)
                        break

            elif event_type == 4 or event_type == 21:  # DUEL OR FOUL COMMITED
                if event_type == 4:
                    # ID 11 = TACKLE, NO SUPPORT FOR AERIAL DUELS
                    if event["duel"]["type"]["id"] == 11:
                        outcome = event["duel"]["outcome"]["name"]
                        if "Lost" in outcome:
                            outcome = False  # FAILED
                        else:
                            outcome = True  # SUCCESS
                if event_type == 21:
                    outcome = False  # FOUL = FAILED
                new_event = Tackle(period, minute, player,
                                   team, location, outcome)
                for p in match.starters+match.subs:
                    if p.id == player:
                        p.events.append(new_event)
                        break

            elif event_type == 10:  # INTERCEPTION
                outcome = event['interception']['outcome']['name']
                if "Lost" in outcome:
                    outcome = False  # FAILED
                else:
                    outcome = True  # SUCCESS
                new_event = Interception(
                    period, minute, player, team, location, outcome)
                for p in match.starters+match.subs:
                    if p.id == player:
                        p.events.append(new_event)
                        break

            elif event_type == 30:  # PASS
                specific = event['pass']
                if 'outcome' in specific:
                    outcome = False  # FAILED
                else:
                    outcome = True  # SUCCESS
                destination = specific['end_location']
                assist = False
                if 'goal_assist' in specific:
                    assist = True
                new_event = Pass(period, minute, player, team,
                                 location, outcome, destination, assist)
                for p in match.starters+match.subs:
                    if p.id == player:
                        p.events.append(new_event)
                        break

            elif event_type == 16:  # SHOT
                outcome = event['shot']['outcome']['id']
                goal = False
                if outcome == 97 or outcome == 100:  # GOAL OR SAVED
                    if outcome == 97:
                        goal = True
                    outcome = True  # ON TARGET
                else:
                    outcome = False  # OFF TARGET
                destination = event['shot']['end_location']
                new_event = Shot(period, minute, player, team,
                                 location, outcome, destination, goal)
                for p in match.starters+match.subs:
                    if p.id == player:
                        p.events.append(new_event)
                        break

            elif event_type == 19:  # SUBSTITUTION
                player = event['substitution']['replacement']
                new_player = Player(
                    player['id'], player['name'], team, None, None)
                match.subs.append(new_player)

    return match
