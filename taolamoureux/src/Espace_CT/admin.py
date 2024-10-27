from django.contrib import admin
from .models import Project, MinecraftServer, CloudTravail

admin.site.register(Project)
admin.site.register(MinecraftServer)
admin.site.register(CloudTravail)