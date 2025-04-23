from rest_framework.test import APITestCase
import json
from datetime import datetime, timezone
from django.contrib.auth.models import User


from agenda.models import Agendamento

class TestListagemAgendamento(APITestCase):
    def test_listagem_vazia(self):
        User.objects.create_user(email="seuze@gmail.com", username="seuze", password="LDM12345678")
        self.client.login(username="seuze", password="LDM12345678")
        response = self.client.get("/api/agendamentos/?username=seuze")
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_listagem_de_agendamento_criados(self): # teste de caso a lista não seja vazia, criar um agendamento e verificar se a resposta foi criada
        seuze = User.objects.create_user(email="seuze@gmail.com", username="seuze", password="LDM12345678")
        self.client.login(username="seuze", password="LDM12345678")
        Agendamento.objects.create(
            data_horario= datetime(2025, 12, 12, tzinfo=timezone.utc),
            nome_cliente= "Teste",
            email_cliente= "rEhRt@example.com",
            telefone_cliente= "00000000000",
            prestador=seuze,

        )
        
        

        agendamento_serializado = {
            "id": 1,
            "data_horario": "2025-12-12T00:00:00Z",
            "nome_cliente": "Teste",
            "email_cliente": "rEhRt@example.com",
            "telefone_cliente": "00000000000",
            "prestador": "seuze",
        }

        response = self.client.get("/api/agendamentos/?username=seuze") # criando um agendamento e enviando os dados
        data = json.loads(response.content)
        self.assertDictEqual(data[0], agendamento_serializado) # verificando se a requisição foi bem sucedida
        
class TestCriacaoAgendamento(APITestCase):
    def test_cria_agendamento(self):
        seuze = User.objects.create_user(email="seuze@gmail.com", username="seuze", password="123")
        agendamento_request_data = {
            "data_horario": "2025-12-12T00:00:00Z",
            "nome_cliente": "Teste",
            "email_cliente": "rEhRt@example.com",
            "telefone_cliente": "00000000000",
            "prestador": "seuze",
        }
        response = self.client.post("/api/agendamentos/", agendamento_request_data)
        self.assertEqual(response.status_code, 201)
        agendamento_criado= Agendamento.objects.get()

        self.assertEqual(agendamento_criado.data_horario, datetime(2025, 12, 12, tzinfo= timezone.utc))
        self.assertEqual(agendamento_criado.prestador, seuze)
    
    def test_cancela_agendamento(self):
        seuze = User.objects.create_user(email="seuze@gmail.com", username="seuze", password="123")
        self.client.login(username="seuze", password="123")
        agendamento_request_data = {
            "data_horario": "2025-12-12T00:00:00Z",
            "nome_cliente": "Teste",
            "email_cliente": "rEhRt@example.com",
            "telefone_cliente": "00000000000",
            "prestador": "seuze",
        }

        # Cria o agendamento via POST
        response = self.client.post("/api/agendamentos/", agendamento_request_data)
        self.assertEqual(response.status_code, 201)

        # Obtém o ID do agendamento criado
        agendamento_id = response.data["id"]

        # Realiza o cancelamento (DELETE)
        delete_response = self.client.delete(f"/api/agendamentos/{agendamento_id}/")
        self.assertEqual(delete_response.status_code, 204)


from unittest import mock
class TestGetHorarios(APITestCase):
    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=True) #decorator, passando o caminho da biblioteca a ser substituida -> substituir a chamada is_feriado vai retornar um obj mock
    def test_quando_data_e_feriado_retorna_lista_vazia(self, _): #utilizado o _ porque condiz com um argumento que não é passado na função
        response = self.client.get('/api/horarios/?data=2022-12-20')
        self.assertEqual(response.data, [])
        
    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=False)
    def test_quando_data_e_dia_comum_retorna_lista_com_horarios(self, _):
        response = self.client.get('/api/horarios/?data=2022-12-25')
        self.assertNotEqual(response.data, [])
        self.assertEqual(response.data[0], datetime(2022, 12, 25, 9, tzinfo=timezone.utc))
        self.assertEqual(response.data[-1], datetime(2022, 12, 25, 17, 30, tzinfo=timezone.utc))
        