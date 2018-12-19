from django.contrib import admin

from .models import Currency, Provider, ServiceArea


class ProviderInline(admin.TabularInline):
    model = Provider


class CurrencyAdmin(admin.ModelAdmin):
    inlines = [
        ProviderInline,
    ]


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Provider)
admin.site.register(ServiceArea)
