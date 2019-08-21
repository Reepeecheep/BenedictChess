from django.urls import path
from Apps.home.views import *

urlpatterns = [
    path('', index, name='index'),
]