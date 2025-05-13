from django.contrib import admin
from .models import Firma

# Register your models here.
class FirmaAdmin(admin.ModelAdmin):
    list_display = ('naziv', 'adresa', 'telefon', 'email', 'web_stranica', 'opis', 'clearance', 'bill')
    search_fields = ('naziv',)
    list_filter = ('clearance',)

admin.site.register(Firma, FirmaAdmin)