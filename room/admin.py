from django.contrib import admin

from .models import Room, Ticket

class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "admin",
        "created_at",
        "is_closed",
        "is_running",
        "min_players",
        "max_players",
    ]
    readonly_fields = [
        "is_closed",
        "is_running",
    ]


class TicketAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "room",
        "issued_to",
        "created_at",
        "is_expired",
        "is_used",
    ]
    readonly_fields = [
        "is_used",
    ]


admin.site.register(Room, RoomAdmin)
admin.site.register(Ticket, TicketAdmin)