from eventapp.serializers import *
from eventapp.models import *
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .validation import Eventinvite,ForgottenPassotp,ForgottenpassMail
from .email import *
from .otp import generate_otp
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# This is Login View user can login with it details it can generate refresh token and accessb token 
# This token time dureaction is refresh token run only 2 hours and access token run only 1 hours
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# all authentications are work on tokens so token are expired so user can't access its permission
# class LogoutView(APIView):
#     pass

    
# only Admin can register here 
class AdminRegisterViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminRegisterSerializer
    permission_classes=[IsAdminUser]
    

# Admin can Add and update, delete, retrive admin user data with filter and paginations
class AdminEventViewset(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends=[SearchFilter,DjangoFilterBackend]
    filterset_fields = ['event_name', 'event_location',"event_city"]
    ordering_fields=("event_name")
    search_fields=('event_name', 'event_location',"event_city")
    permission_classes=[AllowAny]
    

# This is user Event login user can create this event 
class UserEventCreateView(CreateAPIView):
    serializer_class = EventSerializer
    permission_classes=[IsAuthenticated]
    def create(self, request, *args, **kwargs):
        data={
                "event_name":request.data['event_name'],
                "event_location":request.data['event_location'],
                "event_city":request.data['event_city'],
                "event_date":request.data['event_date'],
                "event_time":request.data['event_time'],
                "event_owner":request.user.id
            }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

# User can Update ,delete,retrieve the event data 
class UserEventUpdateView(UpdateAPIView,DestroyAPIView,RetrieveAPIView):
    queryset=Event.objects.all()
    serializer_class = EventSerializer
    permission_classes=[IsAuthenticated]

# user can get list of event 
# user can get list only by his created   
class UserEventListView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes=[IsAuthenticated]
    filter_backends=[SearchFilter,DjangoFilterBackend]
    filterset_fields = ['event_name', 'event_location',"event_city"]
    ordering_fields=["event_name"]
    search_fields=['event_name', 'event_location',"event_city"]
    def get_queryset(self):
        return Event.objects.filter(event_owner=self.request.user)

# user can show the list if invitations
class UserEventInviteListView(ListAPIView):
    serializer_class = EventInviteListSerializer
    permission_classes=[IsAuthenticated]
    filter_backends=[SearchFilter,DjangoFilterBackend]
    filterset_fields = ['event_name', 'event_location',"event_city"]
    ordering_fields=["event_name"]
    search_fields=['event_name', 'event_location',"event_city"]
    def get_queryset(self, request):
        return EventInvite.objects.filter(invite_user=self.request.user) 

# user login after he is Reset password 
class ResetPasswordView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes=[IsAuthenticated]

    def create(self,request):
        user=User.objects.filter(id=request.user.id).first()
        user.set_password(request.data['password'])
        user.save()
        msg=ResetPassEmail(user.email,request.data['password'])
        return Response({"Message":msg})

# it is generate the otp with current username and email both detail are incorrectso otp not generate  
# OTP generate so user id and otp temporary store in session 
# OTP send on register mail id
class OTPView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        (obj,check)=ForgottenPassotp(request.data)
        if check:
            otp=generate_otp()
            request.session['otp'] = otp
            request.session['id']=obj.id
            data=OtpMail(otp,obj)
            return Response({"Message":"OTP Sending on your register mail address"})
        return Response({"Error":"User detail not valid"})

# after opt are generate so currect otp and new password input 
# Both are corrected so the new password reset
class ForgottenPassword(APIView):
    def post(self, request, *args, **kwargs):
        if request.session.get('otp') == request.data['otp']:
            user=User.objects.filter(id=request.session.get('id')).first()
            user.set_password(request.data["password"])
            user.save()
            del request.session['otp'],request.session['id']
            data=ForgottenpassMail(user.email,request.data['password'])
            return Response({"Message":"New Password sending on your mail address "})
        return Response({"error":"Otp invalid"})
    
    
    
# in this API loginuser send to invitations and invitations send so received user get mail
# I have add one features in this API 
# In EventAPI hase 5 records like event_id = 1 ,2,3,4,5
# now testuser are login and he is create a event and this event id is 5
# so he is only send 5 event id event details send not 1,2,3,4 
# he try to send 4 id event so facing the error is "This is not your event"  
class EventInviteViewset(CreateAPIView):
    serializer_class = EventInviteSerializer
    permission_classes=[IsAuthenticated]
    def create(self, request, *args, **kwargs):
        (msg,check)=Eventinvite(request.data,request.user.id)
        if check:
            data={
                "invite_user":request.data['invite_user'],
                "sender_user":request.user.id,
                "event":request.data['event'],
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"Error":msg})
    
# EventInvite Modify     
class EventUpdateInviteViewset(UpdateAPIView,RetrieveAPIView,DestroyAPIView):
    queryset=EventInvite.objects.all()
    serializer_class = EventInviteSerializer
    permission_classes=[IsAuthenticated]

# This API generate the responce about how many invitation send a to another user
class EventInviteListView(ListAPIView):
    serializer_class = EventInviteListSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return EventInvite.objects.filter(sender_user=self.request.user) 
    
    

# This is common user register API and register succesfully so send a  registration successfully mail 
class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data=RegisterMail(request.data)
        response_data = {
            "user": serializer.data,
            "message": "Registration successfully and sending on your registermail"
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

#only admin can show how many user are register
class UserRegisterListView(ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserRegisterView
    filterset_fields = ['first_name', 'last_name',"username","email"]
    permission_classes=[IsAdminUser]



