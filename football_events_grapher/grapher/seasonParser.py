import json


class Match:
    def __init__(self, id, date, home, away, h_score, a_score, mw):
        self.id = id
        self.date = date
        self.home = home
        self.away = away
        self.h_score = h_score
        self.a_score = a_score
        self.mw = mw


def parseMatches(data):
    matches = sorted([Match(m['match_id'], m['match_date'], m['home_team']['home_team_name'], m['away_team']
                            ['away_team_name'], m['home_score'], m['away_score'], m['match_week'])for m in data], key=lambda x: x.mw)

    return matches


# def parseMatches(file):
#     with open(file, encoding="utf8") as f:
#         data = json.load(f)
#         matches = sorted([Match(m['match_id'], m['match_date'], m['home_team']['home_team_name'], m['away_team']
#                                 ['away_team_name'], m['home_score'], m['away_score'], m['match_week'])for m in data], key=lambda x: x.mw)
#     return matches
