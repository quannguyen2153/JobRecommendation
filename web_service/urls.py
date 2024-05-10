from django.contrib import admin
from django.urls import path, include

from api.urls import api_urls
from . import views

urlpatterns = [
  #path('admin/', admin.site.urls),
  path('', views.home),
  path('api/', include(api_urls)),  
]
