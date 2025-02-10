from django.urls import path
from .views import ProfileView, BaseRegisterView, upgrade_me
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'sign'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', 
         LoginView.as_view(template_name = 'sign/login.html'),
         name='login'),
    path('logout/', 
         LogoutView.as_view(template_name = 'sign/logout.html'),
         name='logout'),
    path('signup/', 
         BaseRegisterView.as_view(template_name = 'sign/signup.html'), 
         name='signup'),
     path('upgrade/', upgrade_me, name = 'upgrade'),

]