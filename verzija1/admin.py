from django.contrib import admin
from .models import Firma, Vozilo, FirmaUser, Kvar

# Register your models here.
class FirmaAdmin(admin.ModelAdmin):
    list_display = ('naziv', 'adresa', 'telefon', 'email', 'web_stranica', 'opis', 'clearance', 'bill')
    search_fields = ('naziv',)
    list_filter = ('clearance',)

class VoziloAdmin(admin.ModelAdmin):
    list_display = ('firma', 'naziv', 'tip', 'reg_broj', 'godiste', 'boja', 'kilometri', 'stanje')
    search_fields = ('naziv', 'tip', 'reg_broj')
    list_filter = ('stanje',)

class KvarAdmin(admin.ModelAdmin):
    list_display = ('vozilo', 'opis', 'firma', 'datum_prijave', 'datum_rijesenja', 'cijena_popravka', 'status')
    search_fields = ('vozilo__naziv', 'opis')
    list_filter = ('status',)

class FirmaKorisnikAdmin(admin.ModelAdmin):
    list_display = ('user', 'firma')
    search_fields = ('user__username', 'firma__naziv')

admin.site.register(Firma, FirmaAdmin)
admin.site.register(FirmaUser, FirmaKorisnikAdmin)
admin.site.register(Vozilo, VoziloAdmin)
admin.site.register(Kvar, KvarAdmin)