from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from agenda.models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    prestador = serializers.CharField()
    class Meta:
        model = Agendamento
        fields = '__all__' #expõe todos os dados do modelo, tomar cuidado
   
    def validate_prestador(self, value):
        try:
            prestador_obj = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Username não existe")
        return prestador_obj

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Agendamento não pode ser feito no passado!")
        return value

    def validate(self, attrs):
        telefone_cliente = attrs.get("telefone_cliente", "")
        email_cliente = attrs.get("email_cliente", "")
        if email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
            raise serializers.ValidationError("E-mail brasileiro deve estar associado a um número do Brasil (+55)")
        return attrs

    def create(self, validated_data):
        agendamento = Agendamento.objects.create(
            data_horario = validated_data["data_horario"],
            nome_cliente = validated_data["nome_cliente"],
            email_cliente = validated_data["email_cliente"],
            telefone_cliente = validated_data["telefone_cliente"],
            prestador = validated_data["prestador"]
        )
        return agendamento
    
    # Pode ser utilizado o mesmo serializer para atualização do objeto
    def update(self, instance, validated_data): # self - o próprio obj do serializer, instance - obj do banco de dados, validate_data - os dados da requisição
        instance.data_horario= validated_data.get("data_horario", instance.data_horario) # Vai ser alterado o obj_data horario, vai procurar pela chave da requisição data_horario e caso seja nulo vai pegar o valor do objeto atual
        instance.nome_cliente= validated_data.get("nome_cliente", instance.nome_cliente)
        instance.email_cliente= validated_data.get("email_cliente", instance.email_cliente)
        instance.telefone_cliente= validated_data.get("telefone_cliente", instance.telefone_cliente)
        instance.prestador= validated_data.get("prestador", instance.prestador)
        instance.save() #servindo para salvar no banco de dados as atualizações dos dados realizadas
        return instance
    
class PrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'agendamentos']

    agendamentos = AgendamentoSerializer(many=True, read_only=True)