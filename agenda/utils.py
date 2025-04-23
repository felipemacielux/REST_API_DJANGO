from typing import Iterable
from datetime import date, datetime, timedelta, timezone
from urllib import request

import requests

from agenda.libs import brasil_api
from agenda.models import Agendamento


# definida essa função para que seja utilizada em multiplos lugares
# Função tem objetivo de criar uma lista com horarios disponiveis de 30 em 30 min
def get_horarios_disponiveis(data: date) -> Iterable[datetime]:
    """
    Retorna uma lista com objetos do tipo datetime cujas datas são o mesmo dia passado (data) e os horários são os horários disponíveis para aquele dia, conforme outros agendamentos existam.

    """


    if brasil_api.is_feriado(data): # Para ficar mais fácil do código ser lido separar a API em libs
        return[]



    start = datetime(year=data.year, month=data.month, day=data.day, hour=9, minute=0, tzinfo=timezone.utc)
    end = datetime (year=data.year, month=data.month, day=data.day, hour=18, minute=0, tzinfo=timezone.utc)
    delta = timedelta(minutes=30)
    horarios_disponiveis = set()
    while start < end:
        if not Agendamento.objects.filter(data_horario=start).exists():
            horarios_disponiveis.add(start)
        start = start + delta

    return horarios_disponiveis