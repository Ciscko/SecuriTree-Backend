from django.db import models

# Create your models here.
class Area(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    parent_area = models.ForeignKey("self", null=True, on_delete=models.CASCADE)
    child_area_ids = models.JSONField()

class Door(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name=models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    parent_area = models.ForeignKey(Area, on_delete=models.CASCADE)

class AccessRule(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    doors = models.ManyToManyField(Door)

class Hierarchy(models.Model):
    data = models.JSONField()
