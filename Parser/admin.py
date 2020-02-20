from django.contrib import admin
from .models import Follower, Group, FacebookCredentials


admin.site.register(Group)
admin.site.register(Follower)
admin.site.register(FacebookCredentials)
