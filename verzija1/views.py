from urllib.parse import urlparse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import Registracija, FirmaForma, VoziloForma
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Firma, FirmaUser, Vozilo

@login_required
def home(request):
    try:
        firma_user = FirmaUser.objects.get(user=request.user)
        firma = firma_user.firma
        sazetak_url = urlparse(firma.web_stranica)
        domena = sazetak_url.netloc or sazetak_url.netloc
    except FirmaUser.DoesNotExist:
        firma = { 
            'naziv': 'Trenutno nemate dodjeljenu firmu',
            'opis': 'Molimo vas da kontaktirate administratora za dodjelu firme.',
            'web_stranica': '#',
            }
        domena = None
    return render(request, 'basic.home.html', {'firma': firma, 'domena': domena})

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

@login_required
def vozilo_lista(request):
    vozila = Vozilo.objects.all()
    return render(request, 'basic.vozila.html', {'vozila': vozila})

def vozilo_detail(request, pk):
    vozilo = get_object_or_404(Vozilo, pk=pk)
    return render(request, 'basic.vozilo_info.html', {'vozilo': vozilo})