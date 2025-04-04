from django.contrib import admin

from .models import Room, Ticket

class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "admin",
        "created_at",
        "is_closed",
        "is_finished",
        "min_players",
        "max_players",
    ]
    readonly_fields = [
        "is_closed",
        "is_finished",
    ]
    exclude = ["players"]


class TicketAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "room",
        "share_link",
        "created_at",
        "is_expired",
    ]
    readonly_fields = [
        "created_at",
        "is_expired",
    ]


admin.site.register(Room, RoomAdmin)
admin.site.register(Ticket, TicketAdmin)