from django.db import models

# Create your models here.

class Agendamento(models.Model): #modelo que será criado no banco de dados
    data_horario = models.DateTimeField() # para armazenar datas
    nome_cliente = models.CharField(max_length=100) #quando for incluindo o charfield ele cria um campo de texto com o máximo de 100 caracteres
    email_cliente = models.EmailField()
    telefone_cliente = models.CharField(max_length=20)
    cancelado = models.BooleanField(default=False) # garantir que, por padrão, um agendamento seja considerado ativo (não cancelado) ao ser criado