from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('adminsite/', admin.site.urls),  # default Django admin
    path('', include('tasks.urls')),      # your app urls
]
