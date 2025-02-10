from django.contrib import admin
from django.urls import path, include
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('news.urls', namespace='news')),
    path('sign/', include('sign.urls', namespace='sign')),
    path('accounts/', include('allauth.urls')),
]