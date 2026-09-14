from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_reference",
        "booking",
        "amount",
        "payment_method",
        "status",
    )
    list_filter = ("status", "payment_method")
    search_fields = (
        "transaction_reference",
        "booking__guest__email",
        "booking__property__title",
    )


# Register your models here.
