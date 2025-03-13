from rest_framework import serializers
from agenda.models import Agendamento
from datetime import datetime
from django.utils import timezone 
class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento # Apontando para o modelo que será serializado
        fields = ['id', 'data_horario', 'nome_cliente', 'email_cliente', 'telefone_cliente'] # lista de strings apontando os campos que você deseja colocar no serializer 

#Ocorre o processo de deixar o código sintetizado da forma acima, mas tem o mesmo resultado com que foi criado abaixo

    #data_horario = serializers.DateTimeField()
    #nome_cliente = serializers.CharField(max_length=100)
    #email_cliente = serializers.EmailField()
    #telefone_cliente = serializers.CharField(max_length=20)

    def validate_data_horario(self, value): # depois de executar as validações basicas, vai passar o valor corretamente para o campo com o argumento de value da função
        if value < timezone.now(): #timezone tem a relevância de trazer os horários no momento levando em conta os fusohorarios
            # Precisando destacar a exceção
            raise serializers.ValidationError("Agendamento não pode ser feito no passado!") # para comunicar que houve um erro de validação
        return value
    # validação objlevel, que diz a respeito do serializer como um todo e não apenas a um campo
    def validate(self, attrs):
        telefone_cliente = attrs.get("telefone_cliente", "")
        email_cliente = attrs.get("email_cliente", "")

        if email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"): #metodo swith que questiona se determinada string terminal com algum valor especificado
            raise serializers.ValidationError("E-mail brasileiro deve estar associado a um número do Brasil (+55)")
        return attrs

    def create(self, validated_data):
        agendamento = Agendamento.objects.create(
            data_horario = validated_data["data_horario"],
            nome_cliente = validated_data["nome_cliente"],
            email_cliente = validated_data["email_cliente"],
            telefone_cliente = validated_data["telefone_cliente"]
        )
        return agendamento
    
    # Pode ser utilizado o mesmo serializer para atualização do objeto
    def update(self, instance, validated_data): # self - o próprio obj do serializer, instance - obj do banco de dados, validate_data - os dados da requisição
        instance.data_horario= validated_data.get("data_horario", instance.data_horario) # Vai ser alterado o obj_data horario, vai procurar pela chave da requisição data_horario e caso seja nulo vai pegar o valor do objeto atual
        instance.nome_cliente= validated_data.get("nome_cliente", instance.nome_cliente)
        instance.email_cliente= validated_data.get("email_cliente", instance.email_cliente)
        instance.telefone_cliente= validated_data.get("telefone_cliente", instance.telefone_cliente)
        instance.save() #servindo para salvar no banco de dados as atualizações dos dados realizadas
        return instance