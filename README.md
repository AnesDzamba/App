# DJANGO APP
Prebacujemo citavu aplikaciju na django framework jebat mu mater.\
Kad definisemo sta i kako, treba prvo modele napraviti pa onda view implementirati.\
Vjerovatno cemo se podijeliti jedan za jedan dio drugi za drugi.\
Projekat je kompleksan i jbg ima dosta stavki, moramo osigurati sigurnost i pouzdanost bez da ugrozimo brzinu. Zbog toga treba vidjeti **Django API + React** da se implementira. Jes komplikovano ali moglo bi se.

**NAPOMENA** Glavne settings ne dirati bez mene! I svaki novi model treba migrirati!

**OBAVEZNO KOMENTIRATI KOD !**   
**OBAVEZNO PISATI DEVLOG !**
## Uradjeno - DevLog
Da se fino pise sta je uradjeno i promijene na kodu, da nas sta ne iznenadi kad udjemo.
```
[23.2.2025 23:05] Dzamba - Stvorio Aplikaciju; Kreirao verzija1 kao glavnu aplikaciju; Dodao testni model Viljuskar bez migracije;
[23.2.2025 23:10] Dzamba - Migrirao osnovne stvari; Postavio BP na SQLite3; 
[23.2.2025 00:30] Dzamba - Stvorio ovaj README.md fajl;
[24.2.2025 00:00] Dzamba - Migrirao modele u bazu podataka: Firma, FirmaUser, Ticket;
[24.2.2025 00:13] Dzamba - Napravio Register i Login / Logout sistem sa formom u forms.py, imamo sessions sa csrf tokenima; 
[01.3.2025 03:53] Dzamba - Dodao view za dodavanje firmi i dodao formu koja se prikazuje, treba zavrsiti.
[10.5.2025 00:42] Dzamba - Zavrsio funkcionalnost dodavanje firme kao i njihovo prikazivanje na 'home' dijelu
[10.5.2025 00:45] Dzamba - Dodao prikaz i mogućinost editovanja u admin panelu;
```

## Za uraditi - osnove

> * Definisati hijerarhiju u modelima i websitu
> * Definisati funkcionalnosti koje cemo dodati na pocetku
> * Definisati koje pakete cemo prve uvesti u sistem
> * Definisane modele dodati u bazu preko models.py
> * Razmisliti o pravljenju Django REST API + React


## Objasnjenje
**Kako treba da funkcijonise** - Mi upravljamo Websitom i Bazom Podataka.
Prvi ispod nas su `"Licencirane Firme"` kojima mi dajemo licencu da koriste nase usluge
Oni dovode svoje klijente (npr. Firma se bavi servisiranjem viljuskara i mi njima iznajmljujemo aplikaciju da prate vozila i to sve i oni uvode svoje klijente na kojima vrse servisranje, ugl piramidalna šema.)
Zatim imamo `"Podlicencirane Firme"`, to su firme koje je u sistem unijela `"Licencirana Firma"`.\
Mi zaradjujemo tako sto ovim `"Licenciranim Firmama"` dajemo da koriste usluge nase stranice uz mjesecnu naknadu.

### Mi treba da pruzimo usluge:
> - Upravljanje voznim, prijava kvara, odrzavanje, AI preporuke (gradim model trenutno)
> - Upravljanje paletama u firmi ako ima
> - Upravljanje i izvjestaj paketa na paletama
> - Digitalizacija dokumenata

*Ovo je za pocetak sta trebamo, bit ce jos zahtjeva i profesor mirza je govorio. Al da mi ovo napravimo i mozemo na trziste.*
<hr>

### Baza podataka - info / convo / suggestions
Za pocetak ja bi bazu stavio u **SQLite** ***(VEC STAVLJENO)*** da mozemo lokalno testirati stvari.\
Pa posle prebaciti u **PostgreSQL** da moze podrzati vise unosa posto ce biti puno paleta sa kodovima za pracenje

***ADMIN LOGIN***
```
Username: admin
Password: admin
```
Postavit ce se pravi superuseri al za sad dok nema adekvatne baze, ovo je dovoljno.
<hr>

### Kako postaviti django
**NE POSTAVLJAJ U FOLDERU VEC JE POSTAVLJENO!!** Vec samo da sluzi link ispod kao uvod u sintaksu i funkcije.
>[Prati Tutorijal](https://www.w3schools.com/django/index.php)

Da pokrenes server kucaj `py manage.py runserver`, i vrti ga na localhostu.
<hr>

### Baza podataka - Entity relationship
Ovdje se mora dodati jos puno stvari koje nisu definisane ni na danima logistike.\
Palete i pracenje paketa ostavljamo za kasnije jer niko nije poslao svoje stavke sto je trebao od drugih grupa.\
Tako da boli nas tuki radimo za sad odrzavanje vozila za sta imam definisano vec haman sve.\
**Opste - informacije za sve**
```
User (username,first_name,last_name,email,password,groups,user_permissions,is_staff,is_active,is_superuser,last_login,date_joined)
Firma (firma_id,naziv,clearance,bill,parent)
FirmaUser (user_id,firma_id,clearance)
Ticket (ticket_id,user_id,firma_id,title,content,date_sent,status)
```
**Odrzavanje vozila**
```
Vozilo (vozilo_id,registracija,model,nosivost,god_proizvodnje,snaga_motora,visina_podizanja,tip,cijena,slika)
Kvar (kvar_id,datum,naziv,status,datum_kvara,datum_popravke,vozilo_id)
```