from django.db import models
from django.contrib.auth.models import User

# Definisemo firmu i njene atribute
class Firma(models.Model):
    naziv = models.CharField(max_length=50)
    adresa = models.CharField(max_length=50)
    telefon = models.CharField(max_length=50)
    email = models.EmailField()
    web_stranica = models.URLField()
    opis = models.TextField()
    clearance = models.IntegerField()
    bill = models.DecimalField(max_digits=10, decimal_places=2)
    #parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.naziv}'

# Definisemo zaposlene u firmi i povezujemo usera sa firmom
# Ovo radimo jer ne mozemo dirati MVC definisanu user tabelu
class FirmaUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firma = models.ForeignKey(Firma, on_delete=models.CASCADE)
    ovlastenje = models.IntegerField()  # 0 - admin, 1 - user

    def __str__(self):
        return f'{self.user}, {self.firma}, {self.ovlastenje}'

# Definisemo tickete i povezujemo usera sa firmom    
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firma = models.ForeignKey(Firma, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField()

    def __str__(self):
        return f'{self.user} {self.firma} {self.title} {self.content} {self.date} {self.status}'

class Vozilo(models.Model):
    firma = models.ForeignKey(Firma, on_delete=models.CASCADE)
    naziv = models.CharField(max_length=50)
    tip = models.CharField(max_length=50)
    reg_broj = models.CharField(max_length=20)
    godiste = models.IntegerField()
    boja = models.CharField(max_length=20)
    kilometri = models.IntegerField()
    stanje = models.IntegerField()  # 0 - neispravno, 1 - ispravno, 2 - u servisu
    servis = models.CharField(max_length=50, null=True, blank=True)
    servis_datum = models.DateField(null=True, blank=True)
    servis_kilometri = models.IntegerField(null=True, blank=True)
    servis_cijena = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    servis_opis = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.naziv} {self.tip} {self.reg_broj} {self.godiste} {self.boja}'
    