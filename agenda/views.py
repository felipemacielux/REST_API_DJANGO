from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from requests import request
from agenda.libs.brasil_api import is_feriado
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer
from agenda.utils import get_horarios_disponiveis
from rest_framework import permissions
from django.contrib.auth.models import User


# classe para atuar no nível da API AgendamentoList
class IsOwnerOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        username = request.query_params.get('username', None)
        if request.user.username == username:
            return True
        return False
    
# classe para atuar no nível do obj
class IsPrestador(permissions.BasePermission): # verifica se o usuário que está fazendo requisição é o prestador do agendamento
    def has_object_permission(self, request, view, obj):
        if obj.prestador == request.user:
            return True
        return False

class AgendamentoList(
    generics.ListCreateAPIView
    #mixins.ListModelMixin,  adicionar mixin de listagem --> Faz a listagem de algum objeto ou modelo
    #mixins.CreateModelMixin,  adiconar o mixin de criacao
    #generics.GenericAPIView, classe generica - lida com funcionalidade geral --> request, serializer e queryset
): # cria um método com os nomes de cada um dos HTTPS Methods ---> mixin utilizado para que sejam escritos menos códigos
    
    #Com a classe dessa forma quero que eu seja direcionado para url: /api/agendamentos/?username=felipeverde
    

# Utilizando o generics.ListCreateAPIView não precisa ser utilizado os mixins e não precisa usar os argumentos com as funções abaixo

    serializer_class = AgendamentoSerializer # Apenas para passar a classe
    permission_classes = [IsOwnerOrCreateOnly]
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Agendamento.objects.filter(prestador__username=username) # faz a listagem filtrada  dos objetos(filter) --> utilizado o __ para que seja referenciado
         #metodo utilizado para que seja chamado o queryset
    

    #def get(self, request, *args, **kwargs):
        #return self.list(request, *args, **kwargs) # recebe um request que precisa ser evidenciado com argumentos não nomeados e nomeados, sendo assim a função do self.list é buscar o queryset e serializar
    #def post(self,request, *args, **kwargs):
       # return self.create(request, *args, **kwargs) # Criar objetos a partir de um certo modelo que será no caso o Agendamento


'''@api_view(http_method_names=["GET", "PATCH", "DELETE"])
def agendamento_detail(request, id):
    obj = get_object_or_404(Agendamento, id=id)
    if request.method == "GET":
        serializer = AgendamentoSerializer(obj)
        return JsonResponse(serializer.data)
    if request.method == "PATCH":
        serializer = AgendamentoSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    if request.method == "DELETE":
       obj.delete()
       return Response(status=204)'''

# Para substituição do código acima para que seja transformado em uma classe ----> Class Based Views
    
class AgendamentoDetail(
    generics.RetrieveUpdateDestroyAPIView # Equiavale a cada um dos mixins declarados abaixo
    #mixins.RetrieveModelMixin, # Retrieve tem a mesma ideia do get/buscar o modelo
    #mixins.UpdateModelMixin, # Atualização do objeto
    #mixins.DestroyModelMixin, # Mesma ideia do delete
    #generics.GenericAPIView,
    ):
    permission_classes = [IsPrestador]
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    lookup_field = 'id'
    
    '''lookup_field = 'id' # Corresponde a utilizar o id ao invés do pk que ficaria na url do agendamento/id, porque sem o lookup deve ser passado como pk
    # CRUD
    def get (self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
         
    def patch(self, request, *args, **kwargs):
        return self.partial_update(self, request, *args, **kwargs) # para que seja atualizado os dados de forma parcial
    
    def put (self, request, *args, **kwargs):
        return self.update(self, request, *args, **kwargs)

    def delete(self,request, args, **kwargs): 
        return self.destroy(self, request, *args, **kwargs)
    '''

 
class PrestadorList(
    generics.ListAPIView):

    serializer_class = PrestadorSerializer # Apenas para passar a classe
    queryset = User.objects.all()

@api_view(http_method_names=["GET"])
def get_horarios(request):
    data= request.query_params.get("data")
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()

    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    return Response(horarios_disponiveis)

