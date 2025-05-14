from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import Registracija, FirmaForma
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Firma

@login_required
def home(request):
    firme = Firma.objects.all()
    return render(request, 'basic.home.html', {'firme': firme})

#Da vidim radi li ovo
# klasicni register korisnika
def registracija(request):
    if request.method == 'POST':
        form = Registracija(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Račun je kreiran za {username}! Možete se prijaviti!')
            return redirect('index')
    else:
        form = Registracija()
    return render(request, 'basic.registracija.html', {'form': form})

# Login korisnika
def login_korisnika(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Prijavljeni ste kao <strong>{username}</strong> ( <strong>{user.first_name} {user.last_name}</strong> )')
            return redirect('home')
        else:
            messages.error(request, 'Pogrešno korisničko ime ili lozinka!')
    return render(request, 'basic.login.html')

# Unosis firmu i ispisuje se u 'home'
@login_required
def firma_unos(request):
    if request.method == 'POST':
        form = FirmaForma(request.POST)
        if form.is_valid():
            form.save()
            firma = form.cleaned_data.get('naziv')
            messages.success(request, f'Firma je uspešno dodata! {firma}')
            return redirect('home')
    else:
        form = FirmaForma()
    return render(request, 'admin.firma_unos.html', {'form': form})
