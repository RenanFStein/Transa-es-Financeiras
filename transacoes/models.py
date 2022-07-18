import locale
from msilib.schema import Control
from tkinter import CASCADE
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.forms import CharField



# Create your models here.   
class ImportacoesArquivos(models.Model):
    nome_arquivo = models.CharField(max_length=100)
    tamanho_arquivo = models.CharField(max_length=100 )
    data_importacao_arquivo = models.DateTimeField(auto_now_add=True)
    data_transacao_arquivo = models.DateField(null=False)
    usuario_importacao_arquivo = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome_arquivo

class Controller(models.Model):

    banco_origem = models.CharField (max_length=255, null=False, blank=False)
    agencia_origem = models.CharField (max_length=255, null=False, blank=False)
    conta_origem = models.CharField (max_length=255, null=False, blank=False)

    banco_destino = models.CharField (max_length=255, null=False, blank=False)
    agencia_destino = models.CharField (max_length=255, null=False, blank=False)
    conta_destino = models.CharField (max_length=255, null=False, blank=False)

    valor_da_transacao = models.FloatField(null=False, blank=False)
    data_da_transacao = models.DateField(null=False)
    hora_da_transacao = models.CharField (max_length=255, null=False, blank=False)
    id_arquivo = models.ForeignKey(ImportacoesArquivos, on_delete=models.CASCADE)
    def __str__(self):
        return self.banco_origem



