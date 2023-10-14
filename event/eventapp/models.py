from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Event(models.Model):
    event_name = models.CharField(max_length=200,blank=True,null=True)
    event_location = models.CharField(max_length=500,blank=True,null=True) 
    event_city=models.CharField(max_length=200,blank=True,null=True)
    event_date=models.DateField(blank=True,null=True)
    event_time=models.TimeField(blank=True,null=True)
    event_owner=models.ForeignKey(User,on_delete=models.CASCADE)
    event_create=models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.event_name

class EventInvite(models.Model):
    invite_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invites')
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    invite_status = models.BooleanField(default=True)
    invite_time = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.invite_user.first_name


