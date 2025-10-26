from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registracija, name='registracija'),
    path('login/', views.login_korisnika, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('firma/', views.firma_unos, name='firma_unos'),
    path('unos_vozilo/', views.vozilo_unos, name='vozilo_unos'),
    path('vozila/', views.vozilo_lista, name='vozila'),
    path('vozilo/<int:pk>/', views.vozilo_detail, name='vozilo_detail'),
    path('uposlenici/', views.uposlenici_view, name='uposlenici'),
    path('vozilo_info/<int:pk>/', views.vozilo_info_page, name='vozilo_info_page'),
    path("vozilo_info/<int:pk>/generisi_qr/", views.generisi_qr_view, name="generisi_qr"),
]