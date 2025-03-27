from django.db import models

# Create your models here.

class Agendamento(models.Model): #modelo que será criado no banco de dados
    # o related_name servirá para verificação e direcionamento do usuário ao exemplo de quantos agendamentos foram realizados por ele
    prestador = models.ForeignKey('auth.User', related_name='agendamentos', on_delete=models.CASCADE) # representando uma chave estrangeira que referencia o identificador único (id) de um modelo



    data_horario = models.DateTimeField() # para armazenar datas
    nome_cliente = models.CharField(max_length=100) #quando for incluindo o charfield ele cria um campo de texto com o máximo de 100 caracteres
    email_cliente = models.EmailField()
    telefone_cliente = models.CharField(max_length=20)
    #cancelado = models.BooleanField(default=False) # garantir que, por padrão, um agendamento seja considerado ativo (não cancelado) ao ser criado