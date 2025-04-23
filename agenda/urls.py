from django.urls import path
from agenda.views import AgendamentoList,AgendamentoDetail, PrestadorList, get_horarios

urlpatterns = [
    path('agendamentos/', AgendamentoList.as_view()), # quando é declarado nas URLS precisa coloca .as_view pois se trata de um função em que colocada aqui não reconheceria
    path('agendamentos/<int:id>/', AgendamentoDetail.as_view()), # primeiro parâmetro é para declarar uma rota e o segundo para declarar a view que será chamada quando a API é acessado
    path('horarios/', get_horarios),
    path('prestadores/', PrestadorList.as_view())
]
