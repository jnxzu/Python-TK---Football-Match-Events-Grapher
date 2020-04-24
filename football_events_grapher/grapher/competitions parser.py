import json
import os


class Competition:
    def __init__(self, comp_id, comp, country):
        self.comp_id = comp_id
        self.comp = comp
        self.country = country

    def __hash__(self):
        return hash((self.comp_id, self.comp, self.country))

    def __eq__(self, value):
        return (self.comp_id, self.comp, self.country) == (value.comp_id, value.comp, value.country)

    def __ne__(self, value):
        return not(self == value)


class Season:
    def __init__(self, season_id, season):
        self.season_id = season_id
        self.season_name = season


def parseComps(file):
    with open(file, encoding="utf8") as f:
        comps = {}
        data = json.load(f)
        for d in data:
            comp_id, comp, country, season_id, season = d["competition_id"], d[
                "competition_name"], d["country_name"], d["season_id"], d["season_name"]
            competition = Competition(comp_id, comp, country)
            szn = Season(season_id, season)
            comps.setdefault(competition, []).append(szn)
    return comps


parseComps("competitions.json")
