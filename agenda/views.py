from django.shortcuts import get_object_or_404
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(http_method_names=['GET', 'PATCH', 'DELETE']) # utilizando o recurso da apirest passa a interpretar as views como uma API que retorna em formato json
def agendamento_detail(request, id):
    obj = get_object_or_404(Agendamento, id=id) # na view será buscado o obejto pelo ID
    if request.method == 'GET': #continua com o processo normal de retornar um agendamento
        # serializer faz com que o objeto seja retornado em formato json
        serializer = AgendamentoSerializer(obj) #passando o objeto ele vai tentar encontrar por padrão os dados que foram armazenados no arquivo serializers.py
        return JsonResponse(serializer.data)
    if request.method == 'PATCH': # abre o processo com metodo para editar um agendamento que já existe
        #Precisando validar os itens do objeto para que sejam atualizados
        serializer = AgendamentoSerializer(obj, data=request.data, partial = True) #partial serve para nos informar que o serializer aceita updates parciais, apenas alguns campos sejam passados e o obj precisa ser reconhecido com uma instancia no arquivo serializers
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    if request.method == 'DELETE':
        obj.cancelado = True # para marcar o agendamento como cancelado em vez de deletá-lo
        obj.delete()
        obj.cancelado = True
        return Response(status=204) # status que indica que a resposta não tem um bosy
    
@api_view(http_method_names=['GET', 'POST'])
def agendamento_list(request):
    if request.method == 'GET':
        qs = Agendamento.objects.filter(cancelado=False)
        serializer = AgendamentoSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        data = request.data
        print("Dados recebidos:", data)  # Depuração
        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        print("Erros de validação:", serializer.errors)  # Depuração
        return JsonResponse(serializer.errors, status=400)
    
