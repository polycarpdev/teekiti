from django.contrib import admin
from .models import Payment
from import_export.admin import ImportExportModelAdmin


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'amount', 'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_code', 'user__username', 'event__name')
    readonly_fields = ('transaction_code', 'payment_date')