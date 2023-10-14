from .models import *
from .email import *
from django.contrib.auth.models import User

def Eventinvite(data,id):
    if Event.objects.filter(id=data['event']).exists():
        event=Event.objects.filter(id=data['event']).first()
        if event.event_owner.id == id:
            data=EventinviteMail(id,data["invite_user"])
            return "Done",True
        else:
            return "This is not your event",False
    else:
        return "Event not found",False
    

def ForgottenPassotp(data):
    if User.objects.filter(email=data['email']).exists() and User.objects.filter(username=data['username']).exists():
        user=User.objects.filter(email=data['email']).first()
        return user,True
    else:
        return "None",False
    












