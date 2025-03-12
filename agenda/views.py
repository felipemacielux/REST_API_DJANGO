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
def agendamento_list(request): #vai servir como consulta / será utilizado también para reutilizar essa função, para que se for utilizado um método GET retorna a listagem, mas se for POST ele cria uma nova instância do objeto
    if request.method == 'GET':
        qs = Agendamento.objects.filter(cancelado=False) # Faz com que busque todos os agendamentos 
        serializer = AgendamentoSerializer(qs, many=True) # faz com seja feito uma lista de objetos
        return JsonResponse(serializer.data, safe=False) # para que seja retornado como uma lista e não um simples dicionário precisa ser passado o safe=False 
    if request.method == 'POST':
        data = request.data
        # precisa criar um agendamento a partir do meu objeto, uma nova instancia de agendamento
        serializer = AgendamentoSerializer(data=data) #pega os valores que vierem e verifica se está de acordo com que está explicito no arquivo serializers
        if serializer.is_valid(): 
            serializer.save() # Em algum momento de seu fluxo vai chamar a função create no serializers para criar uma nova instancia da classe 
            return JsonResponse(serializer.data, status=201) # padrão 201 informando que foi criado, siguindo o padrão http created 
        return JsonResponse(serializer.errors, status=400) # padrão 400 informando que houve erro
    
