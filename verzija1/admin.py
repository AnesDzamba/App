from django.contrib import admin
from .models import Firma, Vozilo, FirmaUser

# Register your models here.
class FirmaAdmin(admin.ModelAdmin):
    list_display = ('naziv', 'adresa', 'telefon', 'email', 'web_stranica', 'opis', 'clearance', 'bill')
    search_fields = ('naziv',)
    list_filter = ('clearance',)

admin.site.register(Firma, FirmaAdmin)

class VoziloAdmin(admin.ModelAdmin):
    list_display = ('firma', 'naziv', 'tip', 'reg_broj', 'godiste', 'boja', 'kilometri', 'stanje')
    search_fields = ('naziv', 'tip', 'reg_broj')
    list_filter = ('stanje',)

admin.site.register(Vozilo, VoziloAdmin)

class FirmaKorisnikAdmin(admin.ModelAdmin):
    list_display = ('user', 'firma')
    search_fields = ('user__username', 'firma__naziv')

admin.site.register(FirmaUser, FirmaKorisnikAdmin)