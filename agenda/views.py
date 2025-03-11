from django.shortcuts import get_object_or_404
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Create your views here.
@api_view(http_method_names=['GET', 'PATCH']) # utilizando o recurso da apirest passa a interpretar as views como uma API que retorna em formato json
def agendamento_detail(request, id):
    if request.method == 'GET': #continua com o processo normal de retornar um agendamento
        obj = get_object_or_404(Agendamento, id=id) # na view será buscado o obejto pelo ID
        # serializer faz com que o objeto seja retornado em formato json
        serializer = AgendamentoSerializer(obj) #passando o objeto ele vai tentar encontrar por padrão os dados que foram armazenados no arquivo serializers.py
        return JsonResponse(serializer.data)
    if request.method == 'PATCH': # abre o processo com metodo para editar um agendamento que já existe
        obj = get_object_or_404(Agendamento, id=id) #vou precisar encontrar o objeto no banco de dados
        #Precisando validar os itens do objeto para que sejam atualizados
        serializer = AgendamentoSerializer(data=request.data, partial = True) #partial serve para nos informar que o serializer aceita updates parciais, apenas alguns campos sejam passados
        if serializer.is_valid():
            v_data = serializer.validated_data
            #alterando cada atributo do objeto
            obj.data_horario= v_data.get("data_horario", obj.data_horario) # Vai ser alterado o obj_data horario, vai procurar pela chave da requisição data_horario e caso seja nulo vai pegar o valor do objeto atual
            obj.nome_cliente= v_data.get("nome_cliente", obj.nome_cliente)
            obj.email_cliente= v_data.get("email_cliente", obj.email_cliente)
            obj.telefone_cliente= v_data.get("telefone_cliente", obj.telefone_cliente)
            obj.save() #servindo para salvar no banco de dados as atualizações dos dados realizadas
            return JsonResponse(v_data, status=200)
        return JsonResponse(serializer.errors, status=400)
@api_view(http_method_names=['GET', 'POST'])
def agendamento_list(request): #vai servir como consulta / será utilizado también para reutilizar essa função, para que se for utilizado um método GET retorna a listagem, mas se for POST ele cria uma nova instância do objeto
    if request.method == 'GET':
        qs = Agendamento.objects.all() # Faz com que busque todos os agendamentos 
        serializer = AgendamentoSerializer(qs, many=True) # faz com seja feito uma lista de objetos
        return JsonResponse(serializer.data, safe=False) # para que seja retornado como uma lista e não um simples dicionário precisa ser passado o safe=False 
    if request.method == 'POST':
        data = request.data
        # precisa criar um agendamento a partir do meu objeto, uma nova instancia de agendamento
        serializer = AgendamentoSerializer(data=data) #pega os valores que vierem e verifica se está de acordo com que está explicito no arquivo serializers
        if serializer.is_valid(): 
            validated_data = serializer.validated_data # atributo setado pelo proprio serializer quando o método is_valid() retorna True (criando um dicionario de dados validos)
            Agendamento.objects.create(
                data_horario = validated_data["data_horario"],
                nome_cliente = validated_data["nome_cliente"],
                email_cliente = validated_data["email_cliente"],
                telefone_cliente = validated_data["telefone_cliente"]
            )
            return JsonResponse(serializer.data, status=201) # padrão 201 informando que foi criado, siguindo o padrão http created 
        return JsonResponse(serializer.errors, status=400) # padrão 400 informando que houve erro