from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Firma, Vozilo, FirmaUser

# Definisemo formu za registraciju korisnika
class Registracija(UserCreationForm):
    email = forms.EmailField()
    firma = forms.ModelChoiceField(
        queryset=Firma.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Firma'
    )
    ovlastenje = forms.TypedChoiceField(
        choices=[(1, 'Vlasnik'), (2, 'Serviser'), (3, 'Obicni korisnik')],
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Ovlaštenje'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'firma', 'ovlastenje']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(Registracija, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        if user is not None and user.is_authenticated:
            try:
                firmauser = FirmaUser.objects.get(user=user)
                self.fields['firma'].initial = firmauser.firma
                self.fields['firma'].widget = forms.HiddenInput()
                self.fields['firma'].disabled = True
            except FirmaUser.DoesNotExist:
                pass
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        if commit:
            user.save()
            firma = self.cleaned_data.get('firma')
            ovlastenje = self.cleaned_data.get('ovlastenje')
            FirmaUser.objects.create(user=user, firma=firma, ovlastenje=ovlastenje)
        return user

# Definisemo formu za firmu - unos nove firme u bazu - treba i ovo zavrsiti
class FirmaForma(forms.ModelForm):
    class Meta:
        model = Firma
        fields = ['naziv', 'adresa', 'telefon', 'email', 'web_stranica', 'opis', 'clearance', 'bill']

    def __init__(self, *args, **kwargs):
        super(FirmaForma, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

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
    
class VoziloForma(forms.ModelForm):
    firma = forms.ModelChoiceField(
        queryset=Firma.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Firma'
    )

    class Meta:
        model = Vozilo
        fields = ['firma', 'naziv', 'tip', 'reg_broj', 'godiste', 'boja', 'kilometri', 'stanje', 'servis', 'servis_datum', 'servis_kilometri', 'servis_cijena', 'servis_opis']

    def __init__(self, *args, **kwargs):
        super(VoziloForma, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def save(self, commit=True):
        vozilo = super().save(commit=False)
        if commit:
            vozilo.save()
        return vozilo