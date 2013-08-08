from django.contrib import admin
from marker.models import Team,Player

class TeamAdmin(admin.ModelAdmin):
    fields = ['owner','add_date']
admin.site.register(Team,TeamAdmin)
admin.site.register(Player)
