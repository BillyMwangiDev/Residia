from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "property",
        "guest",
        "check_in_date",
        "check_out_date",
        "status",
        "total_price",
    )
    list_filter = ("status",)
    search_fields = ("property__title", "guest__email")


# Register your models here.
