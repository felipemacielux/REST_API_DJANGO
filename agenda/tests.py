from rest_framework.test import APITestCase
import json
from datetime import datetime, timezone

from agenda.models import Agendamento

class TestListagemAgendamento(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get("/api/agendamentos/")
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_listagem_de_agendamento_criados(self): # teste de caso a lista não seja vazia, criar um agendamento e verificar se a resposta foi criada
        Agendamento.objects.create(
            data_horario= datetime(2025, 12, 12, tzinfo=timezone.utc),
            nome_cliente= "Teste",
            email_cliente= "rEhRt@example.com",
            telefone_cliente= "00000000000",

        )
        
        

        agendamento_serializado = {
            "id": 1,
            "data_horario": "2025-12-12T00:00:00Z",
            "nome_cliente": "Teste",
            "email_cliente": "rEhRt@example.com",
            "telefone_cliente": "00000000000",
        }

        response = self.client.get("/api/agendamentos/") # criando um agendamento e enviando os dados
        data = json.loads(response.content)
        self.assertDictEqual(data[0], agendamento_serializado) # verificando se a requisição foi bem sucedida
        
class TestCriacaoAgendamento(APITestCase):
    def test_cria_agendamento(self):
        agendamento_request_data = {
            "data_horario": "2025-12-12T00:00:00Z",
            "nome_cliente": "Teste",
            "email_cliente": "rEhRt@example.com",
            "telefone_cliente": "00000000000",
        }
        response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")
        

        agendamento_criado= Agendamento.objects.get()

        self.assertEqual(agendamento_criado.data_horario, datetime(2025, 12, 12, tzinfo= timezone.utc))
        self.assertEqual(agendamento_criado.nome_cliente, "Teste")
        self.assertEqual(agendamento_criado.email_cliente, "rEhRt@example.com")
        self.assertEqual(agendamento_criado.telefone_cliente, "00000000000")
    
    def test_quando_request_e_invalido_retorna_400(self):
        ...