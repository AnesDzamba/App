import re
import qrcode
import os
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
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
    
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, 'basic.home.mobile.html', {'firma': firma, 'domena': domena})
    else:
        return render(request, 'basic.home.html', {'firma': firma, 'domena': domena})

# klasicni register korisnika i prosljeđuje poruku za uspješnu registraciju
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

    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, 'basic.registracija.mobile.html', {'form': form})
    else:
        return render(request, 'basic.registracija.html', {'form': form})

# Login korisnika - definisano na ovaj način da mogu formu urediti
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

    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, 'basic.login.mobile.html')
    else:
        return render(request, 'basic.login.html')

# Unos firme u sistem od strane Administrator teama ili korisnika veće privilegije
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
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, 'admin.firma_unos.mobile.html', {'form': form})
    else:
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
                    messages.success(request, 'Vozilo je uspješno dodano!')
                    return redirect('home')
                except Firma.DoesNotExist:
                    messages.error(request, 'Izabrana firma ne postoji.')
            else:
                messages.error(request, 'Morate izabrati firmu.')
    else:
        form = VoziloForma()
    # Prosljeđujemo sve firme u template za prikaz u select polju
    firme = Firma.objects.all()
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, 'admin.vozilo_unos.mobile.html', {'form': form, 'firme': firme})
    else:
        return render(request, 'admin.vozilo_unos.html', {'form': form, 'firme': firme})

@login_required
def vozilo_lista(request):
    # Prikazujemo listu vozila korisniku i pravo prikazujemo detalje
    vozila = Vozilo.objects.all()
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, 'basic.vozila.mobile.html', {'vozila': vozila})
    else:
        return render(request, 'basic.vozila.html', {'vozila': vozila})

@login_required
def vozilo_detail(request, pk):
    # Izvlacimo detalje vozila i prikazujemo korisniku koristeci HTMX
    vozilo = get_object_or_404(Vozilo, pk=pk)
    return render(request, 'basic.vozilo_info.html', {'vozilo': vozilo})

@login_required
def vozilo_info_page(request, pk):
    # Izvlacimo detalje vozila i prikazujemo korisniku na posebnoj stranici
    vozilo = get_object_or_404(Vozilo, pk=pk)
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return render(request, 'basic.vozilo_info_page.mobile.html', {'vozilo': vozilo})
    else:
        return render(request, 'basic.vozilo_info_page.html', {'vozilo': vozilo})

@login_required
def uposlenici_view(request):
    # Povezujemo zaposlenike sa firmom i prikazujemo pripadajucem korisniku firme
    firme = Firma.objects.filter(firmauser__user=request.user).prefetch_related("firmauser_set__user").distinct()
    return render(request, 'basic.uposlenici.html', {'firme': firme})

def generiraj_qr(vozilo, request):
    # napravi URL za vozilo_info_page
    url = request.build_absolute_uri(reverse("vozilo_info_page", args=[vozilo.pk]))

    folder = os.path.join(settings.MEDIA_ROOT, "qr_codes")
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, f"vozilo_{vozilo.pk}.png")

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    # Ovo vraća qrcode.image.pil.PilImage
    pil_img_wrapper = qr.make_image(fill_color="black", back_color="white")

    # Dobijamo pravi PIL.Image.Image objekt
    pil_img = pil_img_wrapper.get_image()

    # Snimamo PNG fajl
    with open(file_path, "wb") as f:
        pil_img.save(f, "PNG")

    vozilo.qr_code.name = f"qr_codes/vozilo_{vozilo.pk}.png"
    vozilo.save()

def generisi_qr_view(request, pk):
    vozilo = get_object_or_404(Vozilo, pk=pk)
    generiraj_qr(vozilo, request)
    html = render_to_string("qr.html", {"vozilo": vozilo})
    return HttpResponse(html)