from django.contrib.auth.models import User as UserModel
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
import json, os
from pathlib import Path
from .models import *
from .data_serializers import *
from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import IsAuthenticated

BASE_DIR = Path(__file__).resolve().parent.parent

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_hierarchy(request):
    """ Return hierarchy data """
    if Hierarchy.objects.all().count() > 0:
        return Response({ 'data' : HierarchySerializer(Hierarchy.objects.all(), many=True).data })
    return Response({ 'data' : 'No data available'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_data(request):
    """ Receives the file from user to upload data to db """
    if('datafile' in request.FILES):
        system_data = store_file(request.FILES['datafile'], 'hierarchy/', BASE_DIR)
        if 'system_data' in system_data and  'areas' in system_data['system_data']and  'doors' in system_data['system_data'] and 'access_rules' in system_data['system_data']:
            delete_data()
            add_data(system_data)
            store_hierarchy()
            """ Return the created data in json format """
            data = dict()
            data["hierarchy"] = HierarchySerializer(Hierarchy.objects.all(), many=True).data
            return Response({ 'status' : 'System data uploaded successfully!' })
        return Response({ 'status' : 'Please upload a file with the correct structure!' })
    return Response({ 'status' : 'Please upload a json file!' })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_users(request):
    """ Receives the file from user to upload data to db """
    if('datafile' in request.FILES):
        users = store_file(request.FILES['datafile'], 'users/', BASE_DIR)
        if 'registered_users' in users:
            users = users['registered_users']
            for user in users:
                found = False
                try:
                   userObj =  UserModel.objects.get(username = user['username'])
                   found = True
                except:
                    pass
                if found:
                    userObj.first_name = user['first_name']
                    userObj.last_name = user['surname']
                    userObj.save()
                    userObj.set_password(user['password'])
                else:
                    UserModel.objects.create_user(
                    first_name = user['first_name'], username  = user['username'],
                    password = user['password'], last_name = user['surname']
                    )
            data = UsersSerializer(UserModel.objects.all(), many=True).data
            return Response({ 'status' : 'Users added successfully!' })
        return Response({ 'status' : 'Please upload a file with the correct structure!' })
    return Response({ 'status' : 'Please upload a json file!' })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doors(request):
    if Door.objects.all().count() > 0:
        return Response({ "data" : DoorSerializer(Door.objects.all(), many=True).data })
    return Response({ "status" : 'No data available' })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = {}
    try:
        user['id'] = request.user.id
        user['email'] = request.user.email
        user['username'] = request.user.username
        return Response({"user" : user})
    except:
        return Response({"user" : 'No user data available in the request, you need to be logged in first!'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lock_door(request):
    if 'door_id' in request.data and 'state' in  request.data:
        door_id = request.data['door_id']
        state = request.data['state']
        found  = False
        try:
            door = Door.objects.get(id = door_id)
            found = True
        except:
            pass
        if found:
            door.status = state
            door.save()
            store_hierarchy()
            return Response({ "status" : "Set successfully"})
        else:
            return Response({ "status" : "Door with that ID does not exist!"})
    return Response({ "status" : "Please set the status and door ID!"})

""" Functions used by the views """
def store_file(thefile, folder, base):
    """ Stores the file in the media folder and returns dictionary data from the file """
    if thefile:
        fs = FileSystemStorage()
        files = fs.listdir(folder)
        for i in files[1]:
            try:
                fs.delete(os.path.join(folder, i))
            except:
                print('Could not delete.'+os.path.join(folder, i))
        sys_file = fs.save(os.path.join(folder, thefile.name), thefile)
        ourfile = base / 'media' / sys_file
        with open(ourfile, 'r') as file:
            data = json.load(file)
            return data
    return None

def store_hierarchy():
    """ Builds the hierarchy object and stores the data """
    data  = read_data()
    for r in data:
        if not r['parent_area'] or r['parent_area'] == None:
            parent = r
    data = create_hierarchy(data, parent)
    Hierarchy.objects.all().delete()
    Hierarchy(data = data).save()


def delete_data():
    """ Delete all the data present in the tables """
    acs = AccessRule.objects.all()
    for ac in acs:
        ac.doors.clear()
    Area.objects.all().delete()
    Door.objects.all().delete()
    AccessRule.objects.all().delete()

def add_data(data):
    """ Receives the data read from json files and stores into db """
    if 'doors' in data['system_data'] and 'areas' in data['system_data'] and 'access_rules' in data['system_data']:
        doors = data['system_data']['doors']
        areas = data['system_data']['areas']
        access_rules = data['system_data']['access_rules']

        """ Transfer each json object into the database """
        for area in areas:
            Area(id = area['id'], name = area['name'], child_area_ids=area["child_area_ids"]).save()

        """ Update each area with it's parent ID """
        for area in areas:
            for child_id in area['child_area_ids']:
                found = False
                try:
                    child_area = Area.objects.get(id = child_id)
                    found = True
                except:
                    pass
                if found:
                    parent = Area.objects.get(id = area['id'])
                    if parent:
                        child_area.parent_area = parent
                        child_area.save()
                    else:
                        print("Area to be assigned as parent does not exist!")
                else:
                    print("Child area with that id does not exist!.")
            
        for door in doors:
            found = False
            try:
                area = Area.objects.get(id =  door['parent_area'])
                found = True
            except:
                pass
            if found:
                Door(id = door['id'], name = door['name'], parent_area = area, status = door['status']).save()
            else:
                print("Parent area not found!")

        for accessrule in access_rules:
            AccessRule(id = accessrule['id'], name = accessrule['name']).save()
            found = False
            try:
                ac = AccessRule.objects.get(id = accessrule['id'])
                found = True
            except:
                pass
            if found:
                for ac_door in accessrule['doors']:
                    foundD = False
                    try:
                        ac_door = Door.objects.get(id = ac_door)
                        foundD = True
                    except:
                        pass
                    if foundD:
                        ac.doors.add(ac_door)
                    else:
                        print("Door object with that id not found.")
                ac.save()
        return True
    return False
   
def read_data():
    doors = DoorSerializer(Door.objects.all(), many=True).data
    areas = AreaSerializer(Area.objects.all(), many=True).data
    access_rules = AccessRulesSerializer(AccessRule.objects.all(), many=True).data 
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
    """ Recursive method to build the hierarchy of nested objects """
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






