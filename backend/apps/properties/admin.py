from django.contrib import admin

from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "host", "location", "price_per_night", "is_active")
    list_filter = ("is_active", "location")
    search_fields = ("title", "description", "location", "host__email")


# Register your models here.
