from django.urls import path
from . import views

urlpatterns = [
    path('index/<group_url>', views.index, name='index'),
    path('send_msg/<msg>', views.send_messages, name='send_messages'),
    path('count_msg', views.count_msg, name='count_msg')
]
