from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader

import football_events_grapher.grapher.competitionsParser as cp
import football_events_grapher.grapher.fileDownloader as fd
import football_events_grapher.grapher.matchParser as mp
import football_events_grapher.grapher.seasonParser as sp

import requests
import json
import os


def landing(request):
    data = requests.get(
        "https://raw.githubusercontent.com/statsbomb/open-data/master/data/competitions.json").json()
    # fd.download(
    #     "https://raw.githubusercontent.com/statsbomb/open-data/master/data/competitions.json")

    comps = cp.parseComps(data)
    template = loader.get_template('landing.html')
    return HttpResponse(template.render({'comps': comps}, request))


def get_seasons(request):
    data = requests.get(
        "https://raw.githubusercontent.com/statsbomb/open-data/master/data/competitions.json").json()

    comp = int(request.POST['comp_id'])
    szns = cp.parseSeasons(data, comp)
    return JsonResponse([s.__dict__ for s in szns], safe=False)


def get_matches(request):
    comp_id, szn_id = request.POST['comp_id'], request.POST['season_id']
    base_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/"
    szn_url = base_url + comp_id + "/" + szn_id + ".json"

    data = requests.get(szn_url).json()
    # fd.download(szn_url)

    matches = sp.parseMatches(data)
    # os.remove(szn_id + ".json")
    return JsonResponse([m.__dict__ for m in matches], safe=False)


def main(request):
    match_id = request.GET['match_id']
    base_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/"
    match_url = base_url + match_id + ".json"

    data = requests.get(match_url).json()
    # fd.download(match_url)

    match = mp.parseEvents(data)
    # os.remove(match_id + ".json")
    template = loader.get_template('main.html')
    match_serialized = json.dumps(
        match.__dict__, default=lambda o: o.__dict__, indent=4)
    return HttpResponse(template.render({'match_serial': match_serialized, 'match': match}, request))
