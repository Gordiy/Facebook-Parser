from django.urls import path
from . import views

urlpatterns = [
    path('index/<group_url>', views.index, name='index')
]