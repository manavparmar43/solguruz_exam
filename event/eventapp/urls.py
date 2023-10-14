from eventapp.views import *
from rest_framework.routers import DefaultRouter
from django.urls import path,include

router = DefaultRouter()

router.register('admin-register', AdminRegisterViewset, basename='admin-register'),
router.register('admin-event', AdminEventViewset, basename='event'),





urlpatterns = [
    path("",include(router.urls)),
    path('login/',LoginView.as_view(), name='login'), 
    path('user-list/',UserRegisterListView.as_view(), name='user-list'), 
    path('invite-event/', EventInviteViewset.as_view(), name='invite-event'),
    path('invite-event-update-delete/<int:pk>/', EventUpdateInviteViewset.as_view(), name='invite-event-update-delete'),
    path('send-eventinvite-list/', EventInviteListView.as_view(), name='send-eventinvite-list'),
    path("user-register/",UserRegisterView.as_view(),name="user-register"),
    path("user-event/",UserEventCreateView.as_view(),name="user-event"),
    path("user-event-list/",UserEventListView.as_view(),name="user-event-list"),
    path("user-eventinvite-list/",UserEventInviteListView.as_view(),name="user-eventinvite-list"),
    path("reset-password/",ResetPasswordView.as_view(),name="reset-password"),
    path("user-event-update-delete/<int:pk>/",UserEventUpdateView.as_view(),name="user-event-update-delete"),
    path("otp/",OTPView.as_view(),name="otp"),
    path("forgottenpass/",ForgottenPassword.as_view(),name="forgottenpass"),



]