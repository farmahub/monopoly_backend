from django.contrib import admin

from .models import Property


class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        "position",
        "name",
        "color",
        "type",
        "price",
        "rent_single",
        "rent_set",
        "rent_1",
        "rent_2",
        "rent_3",
        "rent_4",
        "rent_5",
        "loan_amount",
        "loan_back_amount",
        "house_price",
        "hotel_price",
        "owner",
    ]
    list_display_links = ('position','name',)
    ordering = ["position",]


admin.site.register(Property, PropertyAdmin)
