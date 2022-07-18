from django.urls import path
from . import views

urlpatterns = [
    path('transacoes/', views.transacoes, name='transacoes'),
    path('analise_de_transacoes/', views.analise_de_transacoes, name='analise_de_transacoes'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/delete_user', views.delete_user, name='delete_user'),
    path('usuarios/update_user', views.update_user, name='update_user'),
    path('usuarios/new_user', views.new_user, name='new_user'),
]

