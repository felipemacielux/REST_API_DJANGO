from rest_framework.test import APITestCase
import json
from datetime import datetime
from django.utils.timezone import make_aware
from agenda.models import Agendamento


class TestListagemAgendamentos(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get("/api/agendamentos/")
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_listagem_de_agendamentos_criados(self):
        agendamento = Agendamento.objects.create(
            data_horario=make_aware(datetime(2025, 3, 19)),
            nome_cliente="Alice",
            email_cliente="alice@email.com",
            telefone_cliente="999988888",
        )

        agendamento_serializado = {
            "id": agendamento.id,
            "data_horario": "2025-03-19T00:00:00Z",
            "nome_cliente": "Alice",
            "email_cliente": "alice@email.com",
            "telefone_cliente": "999988888",
            "cancelado": False  # Adicionado o campo cancelado
        }

        response = self.client.get("/api/agendamentos/")
        data = json.loads(response.content)
        self.assertDictEqual(data[0], agendamento_serializado)


class TestCriacaoAgendamento(APITestCase):
    def test_cria_agendamento(self):
        agendamento_request_data = {
            "data_horario": "2025-03-19T00:00:00Z",  # Data futura
            "nome_cliente": "Alice",
            "email_cliente": "alice@email.com",
            "telefone_cliente": "999988888"
        }
        response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")
        
        # Depuração: Imprime o conteúdo da resposta
        print(response.content)
        
        self.assertEqual(response.status_code, 201)

        agendamento_criado = Agendamento.objects.first()
        self.assertIsNotNone(agendamento_criado)
        self.assertEqual(agendamento_criado.nome_cliente, "Alice")
        self.assertEqual(agendamento_criado.email_cliente, "alice@email.com")
        self.assertEqual(agendamento_criado.telefone_cliente, "999988888")

        data_horario_esperada = make_aware(datetime(2025, 3, 19))  # Data futura
        self.assertEqual(agendamento_criado.data_horario, data_horario_esperada)