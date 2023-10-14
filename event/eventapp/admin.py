from django.contrib import admin
from .models import *

@admin.register(Event)
class Events(admin.ModelAdmin):
        list_display=['id','event_name','event_location','event_date','event_time','event_owner','event_create']

@admin.register(EventInvite)
class EventInvite(admin.ModelAdmin):
        list_display=['id','invite_user','invite_status','invite_time','event',"sender_user"]