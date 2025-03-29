from django.contrib import admin

from .models import Player

class PlayerAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "position", "cash", "jail_free_card", "house", "hotel"]

admin.site.register(Player, PlayerAdmin)