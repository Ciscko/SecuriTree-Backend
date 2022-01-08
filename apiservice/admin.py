from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'parent_area']
    
@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
	list_display = ['id', 'name','status', 'parent_area']

@admin.register(AccessRule)
class ACAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']

@admin.register(Hierarchy)
class HierarchyAdmin(admin.ModelAdmin):
	list_display = ['id', 'data']