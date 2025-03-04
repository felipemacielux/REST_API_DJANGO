from django.shortcuts import get_object_or_404
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Create your views here.
@api_view(http_method_names=['GET']) # utilizando o recurso da apirest passa a interpretar as views como uma API que retorna em formato json
def agendamento_detail(request, id):
    obj = get_object_or_404(Agendamento, id=id) # na view será buscado o obejto pelo ID
    # serializer faz com que o objeto seja retornado em formato json
    serializer = AgendamentoSerializer(obj) #passando o objeto ele vai tentar encontrar por padrão os dados que foram armazenados no arquivo serializers.py
    return JsonResponse(serializer.data)

@api_view(http_method_names=['GET'])
def agendamento_list(request): #vai servir como consulta 
    qs = Agendamento.objects.all() # Faz com que busque todos os agendamentos 
    serializer = AgendamentoSerializer(qs, many=True) # faz com seja feito uma lista de objetos
    return JsonResponse(serializer.data, safe=False) # para que seja retornado como uma lista e não um simples dicionário precisa ser passado o safe=False