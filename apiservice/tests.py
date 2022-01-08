from django.test import TestCase,  Client 
from .models import *
from .views import *
import os
# Create your tests here.
BASE_DIR = Path(__file__).resolve().parent.parent
sys_file = BASE_DIR  / 'media/json_data/system_data_schema.json'
users_file = BASE_DIR / 'media/json_data/registered_users.json'
#Models' TESTS
class ModelsTest(TestCase):
    """ Tests for all the models """
    def setUp(self):
        Area(id = '1', name="Area 1", child_area_ids = ['2']).save()
        self.a1 = Area.objects.get(id = '1')
        Area(id = '2', name="Area 2", child_area_ids = ['3'], parent_area = self.a1).save()
        self.a2 = Area.objects.get(id = '2')

        Door(id = '1', name = 'Door 1', parent_area = self.a1, status = 'open' ).save()
        Door(id = '2', name = 'Door 2', parent_area  = self.a1, status = 'closed' ).save()
        self.d1 = Door.objects.get(id = '1')
        self.d2 = Door.objects.get(id = '2')

        AccessRule(id = '1', name = 'AC 1').save()
        self.ac1  = AccessRule.objects.get(id = '1')
        self.ac1.doors.add(self.d1, self.d2)
        self.ac1  = AccessRule.objects.get(id = '1')
        
    def test_create_areas(self):
        self.assertEqual(Area.objects.count(), 2)
        self.assertIsInstance(self.a1, Area, 'Area not of that class')

    def test_create_doors(self):
        self.assertTrue(Door.objects.all().count() == 2)
        self.assertIsInstance(self.d1, Door, 'Door 1 not of that class')
        self.assertIsInstance(self.d2, Door, 'Door 2 not of that class')

    def test_create_access_rules(self):
        self.assertTrue(AccessRule.objects.all().count() == 1)
        self.assertIsInstance(self.ac1, AccessRule, 'AccessRule not of that class')
        
#*********************  VIEWS'TESTS   **************************
class ViewsTests(TestCase):
    """ Tests for all the views file functions"""
    def setUp(self):
        Area(id = '1', name="Area 1", child_area_ids = ['2']).save()
        self.a1 = Area.objects.get(id = '1')
        Area(id = '2', name="Area 2", child_area_ids = ['3'], parent_area = self.a1).save()
        self.a2 = Area.objects.get(id = '2')

        Door(id = '1', name = 'Door 1', parent_area = self.a1, status = 'open' ).save()
        Door(id = '2', name = 'Door 2', parent_area  = self.a1, status = 'closed' ).save()
        self.d1 = Door.objects.get(id = '1')
        self.d2 = Door.objects.get(id = '2')

        AccessRule(id = '1', name = 'AC 1').save()
        self.ac1  = AccessRule.objects.get(id = '1')
        self.ac1.doors.add(self.d1, self.d2)
        self.ac1  = AccessRule.objects.get(id = '1')

        self.client = Client()
        

    def test_get_hierarchy(self):
        """ Test response for empty db """
        response = self.client.get('/api/')
        self.assertTrue( 'data' in response.data )
        self.assertTrue( 'No data available' in response.data['data'] )
        store_hierarchy()
        """ Test response for presence of keys in data """
        response = self.client.get('/api/')
        self.assertTrue(response.status_code == 200)
        #print(response.data['data'][0]['data'])
        self.assertTrue( 'child_areas' in response.data['data'][0]['data'] )
        """ Test if parent area has NULL parent area """
        self.assertTrue( not response.data['data'][0]['data']['parent_area'] )
    
    def test_upload_data(self):
        res = self.client.post('/api/upload/', { })
        print(res.data)
        self.assertTrue(res.status_code == 200)
        self.assertTrue('Please upload a json file' in res.data['status'])

        with open(users_file, 'rb') as f:
            res = self.client.post('/api/upload/', { 'datafile' : f})
        self.assertTrue(res.status_code == 200)
        print(res.data)
        self.assertTrue('structure' in res.data['status'])

        with open(sys_file, 'rb') as f:
            res = self.client.post('/api/upload/', { 'datafile' : f})
        print(res.data)
        self.assertTrue(res.status_code == 200)
        self.assertTrue('System data uploaded successfully' in res.data['status'])
    
    def test_upload_users(self):
        res = self.client.post('/api/upload_users/', { })
        #print(res.data)
        self.assertTrue(res.status_code == 200)
        self.assertTrue('Please upload a json file' in res.data['status'])

        with open(sys_file, 'rb') as f:
            res = self.client.post('/api/upload_users/', { 'datafile' : f})
        self.assertTrue(res.status_code == 200)
        #print(res.data)
        self.assertTrue('structure' in res.data['status'])

        with open(users_file, 'rb') as f:
            res = self.client.post('/api/upload_users/', { 'datafile' : f})
        #print(res.data)
        self.assertTrue(res.status_code == 200)
        self.assertTrue('successfully' in res.data['status'])
        
    def test_get_doors(self):
        res = self.client.get('/api/doors/')
        self.assertTrue(res.status_code == 200)

    def test_get_user(self):
        res = self.client.get('/api/user/')
        msg = 'No user data available in the request, you need to be logged in first!'
        self.assertTrue(res.status_code == 200)
        self.assertTrue(res.data['user'] == msg)
    
    def test_lock_door(self):
        res = self.client.get('/api/lock_door/', {})
        self.assertTrue(res.status_code != 200)
        
        res = self.client.post('/api/lock_door/', {})
        self.assertTrue(res.status_code == 200)
        self.assertTrue(res.data['status'] == 'Please set the status and door ID!')

        res = self.client.post('/api/lock_door/', {'door_id' : '1', 'state': 'closed'})
        self.assertTrue(res.status_code == 200)
        self.assertTrue('successfully' in res.data['status'])
        
        d = Door.objects.get(id = '1')
        self.assertTrue(d.status == 'closed')


    def test_delete_data(self):
        """ Test if the delete function is emptying db """
        a1 = Area.objects.all().count()
        d1 = Door.objects.all().count()
        ac1 = AccessRule.objects.all().count()
        self.assertTrue(a1 != 0)
        self.assertTrue(d1 != 0)
        self.assertTrue(ac1 != 0)
        delete_data()
        a2 = Area.objects.all().count()
        d2 = Door.objects.all().count()
        ac2 = AccessRule.objects.all().count()
        self.assertTrue(a2 == 0)
        self.assertTrue(d2 == 0)
        self.assertTrue(ac2 == 0)

    def test_store_file(self):
        """ Test the file is stored successfully and data read from it """
        with open(users_file, 'rb') as f:
            data = store_file(f, 'users/', BASE_DIR)
        self.assertTrue('registered_users' in data)
        with open(sys_file, 'rb') as f:
            data = store_file(f, 'hierarchy/', BASE_DIR)
        self.assertTrue('system_data' in data)

    def test_read_data(self):
        """  Test that returned list of dictionary data contains all the appended keys """
        data = read_data()
        for i in data:
            self.assertTrue('id' in i and 'name' in i and 'parent_area' in i and 'access_rules' in i and 'doors' in i)

    def test_add_data(self):
        """ Test data read from files is stored in db and  correctly """
        delete_data()
        with open(sys_file, 'rb') as f:
            data = store_file(f, 'hierarchy/', BASE_DIR)
            response1 = add_data({'system_data': {'areas': [], 'doors' : [], 'access_rules' : []}})
            areas = Area.objects.all()
            self.assertEquals(areas.count(), 0)
            response2 = add_data(data)
            areas = Area.objects.all()
            self.assertEquals(areas.count(), 18)
            self.assertTrue(response1)
            self.assertTrue(response2)
            
    def test_store_hierarchy(self):
        """ Test if the hierarchy data is stored afresh each time """
        Hierarchy.objects.all().delete()
        self.assertTrue(Hierarchy.objects.all().count() == 0)
        store_hierarchy()
        print(type(Hierarchy.objects.all()))
        self.assertTrue(Hierarchy.objects.all().count() == 1)
        





