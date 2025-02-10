from django.contrib import admin
from django.urls import path, include

 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('news.urls', namespace='news')),
    path('sign/', include('sign.urls', namespace='sign')),
    path('accounts/', include('allauth.urls')),

    path('accounts/yandex/login/', include('allauth.socialaccount.urls')),
    path('accounts/login/', include('allauth.account.urls'), name='accounts_login'),
    path('accounts/signup/', include('allauth.account.urls'), name='account_signup'),
    path('accounts/password/reset/', include('allauth.account.urls'), name='account_reset_password'),
    path('accounts/password/reset/done/', include('allauth.account.urls'), name='account_reset_password_done'),
    path('accounts/password/change/', include('allauth.account.urls'), name='account_change_password_done'),
    path('accounts/password/change/done/', include('allauth.account.urls'), name='account_change_password_done'),
]