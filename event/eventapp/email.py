
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import *

def ResetPassEmail(email,password):
    subject = 'Password Reset Request'
    message = f'Your  reset password {password}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email],fail_silently=False)
    return "Successfully password reset and mail send on register mail address"


def EventinviteMail(sender_id,received_id):
    sender_user=User.objects.filter(id=sender_id).first()
    receiv_user=User.objects.filter(id=received_id).first()
    event=Event.objects.filter(event_owner__id=sender_id).first()
    name=str(sender_user.first_name) + " " + str(sender_user.last_name)
    subject = f'Event Invitation for {name}'
    message = f'Event Name: {event.event_name}  Event Location: {event.event_location} Event City: {event.event_city} Event Date: {event.event_date} Event Time: {event.event_time} '
    send_mail(subject, message, settings.EMAIL_HOST_USER, [receiv_user.email],fail_silently=False)
    return True

def RegisterMail(data):

    subject = f'Register Successfully'
    message = f'Your Register Done'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [data['email']],fail_silently=False)
    return True

def OtpMail(otp,obj):

    subject = f'OTP Infomation'
    message = f'Your Otp:{otp}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [obj.email],fail_silently=False)
    return True

def ForgottenpassMail(email,password):

    subject = f'Forgottenpassword Infomation'
    message = f'Your New Password:{password}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email],fail_silently=False)
    return True