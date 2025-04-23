from datetime import date
import requests
from django.conf import settings # declarado em settings.py
import logging
def is_feriado(date: date): 
    logging.info(f"Fazendo a requisição para o BrasilAPI para a data: {date.isoformat()}")
    if settings.TESTING == True: # Segregar mais o teste para que possa cravar de forma mais precisa, ou seja qualquer requisição feita para is_feriado não fará requisição para API externa
        logging.info(f"Requisição não está sendo feita pois TESTING = True") # irá mostrar issos nos logs
        if date.day == 25 and date.month == 12:
            return True
        return False
    # Chamar a API Brascil com ano da data
    # Verificar se os feriados retornados possuem a data igual a data solicitada pelo nosso usuário
    # Caso afirmativo: retorna uma lista vazia 
    ano = date.year # retorna o ano daquele objeto
    r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
    if not r.status_code == 200: # operador de diferença para que possamos saber se deu erro na requisição
        logging.error("Algum erro ocorreu na Brasil API") #exemplo caso o site fique fora do ar 
        return False
        #raise ValueError ("Não foi possível consultar os feriados")
    feriados = r.json()
    for feriado in feriados:
        data_feriado_as_str = feriado ["date"]
        # data que veio da requisição para transformar em um objeto do tipo data
        data_feriado = date.fromisoformat(data_feriado_as_str) # "2020-01-30" => date(2020, 1, 30)
        if date == data_feriado:
            return True # para retornar uma lista vazia para os horários disponíveis para as datas com feriados
    return False