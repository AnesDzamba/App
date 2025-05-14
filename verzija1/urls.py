from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registracija, name='registracija'),
    path('login/', views.login_korisnika, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('firma/', views.firma_unos, name='firma_unos'),
]