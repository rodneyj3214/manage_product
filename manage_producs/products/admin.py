from django.contrib import admin

# Register your models here.
from manage_producs.products.models import HistorySearchProduct


@admin.register(HistorySearchProduct)
class HistoryProductAdmin(admin.ModelAdmin):
    list_display = [
        "ip_address",
        "creation_date",
        "product",
    ]

    search_fields = ["product"]
