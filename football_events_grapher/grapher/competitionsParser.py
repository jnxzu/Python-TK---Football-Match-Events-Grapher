import json
import os


class Competition:
    def __init__(self, comp_id, comp, country):
        self.comp_id = comp_id
        self.comp = comp
        self.country = country

    def __hash__(self):
        return hash(self.comp_id)

    def __eq__(self, value):
        return self.comp_id == value.comp_id

    def __ne__(self, value):
        return not(self == value)


class Season:
    def __init__(self, season_id, season):
        self.season_id = season_id
        self.season_name = season


def parseComps(file):
    with open(file, encoding="utf8") as f:
        comps = []
        data = json.load(f)
        for d in data:
            comp_id, comp, country = d["competition_id"], d[
                "competition_name"], d["country_name"]
            competition = Competition(comp_id, comp, country)
            if competition not in comps:
                comps.append(competition)
    return comps


def parseSeasons(file, comp):
    with open(file, encoding="utf8") as f:
        szns = []
        data = json.load(f)
        for d in data:
            comp_id, szn_id, season = d["competition_id"], d["season_id"], d[
                "season_name"]
            szn = Season(szn_id, season)
            if comp_id == comp:
                szns.append(szn)
    return szns
