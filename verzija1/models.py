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
        return f'{self.naziv} {self.adresa} {self.telefon} {self.email} {self.web_stranica} {self.opis}'

# Definisemo zaposlene u firmi i povezujemo usera sa firmom
# Ovo radimo jer ne mozemo dirati MVC definisanu user tabelu
class FirmaUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firma = models.ForeignKey(Firma, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} {self.firma}'

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

