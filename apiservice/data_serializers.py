from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User as UserModel

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'
    
class DoorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door
        fields = '__all__'

class AccessRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRule
        fields = '__all__'

class HierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hierarchy
        fields = ['data']

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'