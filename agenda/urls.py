from django.urls import path
from agenda.views import agendamento_detail
from agenda.views import agendamento_list

urlpatterns = [
    path('agendamentos/', agendamento_list),
    path('agendamentos/<int:id>/', agendamento_detail), # primeiro parâmetro é para declarar uma rota e o segundo para declarar a view que será chamada quando a API é acessado
]
