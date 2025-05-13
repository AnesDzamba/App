from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Firma

# Definisemo formu za registraciju korisnika
class Registracija(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        if commit:
            user.save()
        return User

# Definisemo formu za firmu - unos nove firme u bazu - treba i ovo zavrsiti
class FirmaForma(forms.ModelForm):
    class Meta:
        model = Firma
        fields = ['naziv', 'adresa', 'telefon', 'email', 'web_stranica', 'opis', 'clearance', 'bill']
    
    def save(self, commit = True):
        firma = super().save(commit=False)
        firma.naziv = self.cleaned_data.get('naziv')
        firma.adresa = self.cleaned_data.get('adresa')
        firma.telefon = self.cleaned_data.get('telefon')
        firma.email = self.cleaned_data.get('email')
        firma.web_stranica = self.cleaned_data.get('web_stranica')
        firma.opis = self.cleaned_data.get('opis')
        firma.clearance = self.cleaned_data.get('clearance')
        firma.bill = self.cleaned_data.get('bill')
        if commit:
            firma.save()
        return Firma