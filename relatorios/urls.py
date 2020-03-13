from django.urls import path
from . import views



urlpatterns = [
    path('todasvistorias', views.todasvistorias, name='todasvistorias'),
    path('', views.minhasvistorias, name='minhasvistorias'),
    path('vistoria/<int:pk>', views.vistoriadetalhes, name='vistoriadetalhes'),
    path('deferir/<int:pk>', views.deferir, name='deferir'),
    path('indeferir/<int:pk>', views.indeferir, name='indeferir'),
    path('vistoria_pdf/<int:pk>', views.vistoria_pdf, name='vistoria_pdf'),
    path('ajuda/', views.ajuda, name='ajuda'),
]
