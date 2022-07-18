from django.contrib import admin
from django.forms import ModelForm
from .models import Controller, ImportacoesArquivos

from django.utils.formats import localize 
import locale
# Register your models here.

@admin.register(ImportacoesArquivos)
class ImportacoesArquivosAdmin(admin.ModelAdmin): 
                                
    list_display = ('nome_arquivo',  
                    'tamanho_arquivo', 
                    'data_importacao_arquivo', 
                    'data_transacao_arquivo',
                    'usuario_importacao_arquivo')

@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin): 
                                
    list_display = ('banco_origem',  
                    'agencia_origem', 
                    'conta_origem', 

                    'banco_destino',
                    'agencia_destino', 
                    'conta_destino',

                    'valor_da_transacao',
                    'data_da_transacao',
                    'hora_da_transacao',
                    'id_arquivo')



