from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import Registracija, FirmaForma, VoziloForma
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
            return redirect('home')
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

@login_required
def vozilo_unos(request):
    if request.method == 'POST':
        form = VoziloForma(request.POST)
        if form.is_valid():
            vozilo = form.save(commit=False)
            # Pretpostavljamo da korisnik bira firmu iz forme (npr. select polje)
            # ili prosleđuje ID firme kroz POST podatke
            firma_id = request.POST.get('firma')
            if firma_id:
                try:
                    firma = Firma.objects.get(id=firma_id)
                    vozilo.firma = firma
                    vozilo.save()
                    messages.success(request, 'Vozilo je uspešno dodato!')
                    return redirect('home')
                except Firma.DoesNotExist:
                    messages.error(request, 'Izabrana firma ne postoji.')
            else:
                messages.error(request, 'Morate izabrati firmu.')
    else:
        form = VoziloForma()
    # Prosleđujemo sve firme u template za prikaz u select polju
    firme = Firma.objects.all()
    return render(request, 'admin.vozilo_unos.html', {'form': form, 'firme': firme})