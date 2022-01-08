from django.shortcuts import render
import json
from pathlib import Path
# Create your views here.
BASE_DIR = Path(__file__).resolve().parent.parent
system_data = BASE_DIR / 'json_data/system_data.json'
hdata = BASE_DIR / 'json_data/hdata.json'

areass = []
doors = []
access_rules = []


def index(request):
    return render(request, 'index.html')


def read_data():
    with open(system_data, 'r') as file:
        data = json.load(file)
        doors = data['system_data']['doors']
        areas = data['system_data']['areas']
        access_rules = data['system_data']['access_rules']
        for door in doors:
            door['access_rules'] = []
            for rule in access_rules:
                if(door['id'] in rule['doors']):
                    door['access_rules'].append({"id": rule['id'], "name" : rule['name']})
        for area in areas:
            area['doors'] = []
            ac_set = set([])
            area['access_rules'] = []
            for door in doors:
                if(door['parent_area'] == area['id']):
                    area['doors'].append({"id":door['id'], "name" : door['name'], "status" : door['status']})
                    for access_rule in door['access_rules']:
                        ac_set.add(access_rule['name'])
            area['access_rules'] = list(ac_set)
        return areas


def create_hierarchy(areas, dic):
    if(len(dic['child_area_ids']) < 1):
        return dic
    else:
        child = {}
        dic['child_areas'] = []
        for id in dic['child_area_ids']:
            for area in areas:
                if(id == area['id']):
                    child = area
                    dic['child_areas'].append(create_hierarchy(areas, child))
        return dic

#data  = read_data()
""" data = []
print(len(data)) 
js = create_hierarchy(data, data[0])
with open(hdata, 'w') as f:
    json.dump(js, f) """



