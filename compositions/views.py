from django.shortcuts import render, get_object_or_404, redirect
from .models import Composition, CostHistory, Insumo, State, CompositionInsumo, Classe, Grupo
from rest_framework import viewsets, status
from django.core.paginator import Paginator
from .serializers import CompositionSerializer, CompositionDetailSerializer, InsumoSerializer, CostHistorySerializer
from django.db.models import Q, Count, F, ExpressionWrapper, fields, Prefetch, Case, When, Value, CharField, IntegerField, Count
from django.db.models.functions import Lower
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import ListView
from collections import defaultdict



def home_view(request):
    return render(request, 'home.html')
    

def composition_detail(request, codigo):
    composition = get_object_or_404(Composition, codigo=codigo)
    composition_insumos = CompositionInsumo.objects.filter(composition=composition).select_related('insumo')


    state = State.objects.get(id=1)
    insumo_data = []

    for comp_insumo in composition_insumos:
        insumo = comp_insumo.insumo
        quantity = comp_insumo.quantity

    

        insumo_data.append({
            'insumo': insumo,
            'quantity': quantity,
        })

    context = {
        'composition': composition,
        'grupo': composition.grupo,
        'insumo_data': insumo_data,
    }



    return render(request, 'compositions/composition_detail.html', context)



def composition_list(request):
    compositions = Composition.objects.all()

    for composition in compositions:
        composition.num_children = composition.compositionchild_set.count()
        composition.num_insumos = composition.compositioninsumo_set.count()
        composition.total_children = composition.num_children + composition.num_insumos

    return render(request, 'compositions/composition_list.html', {'compositions': compositions})




def insumo_list_view(request):
    query = request.GET.get('q', '')
    if query:
        try:
            # If the query can be cast to an int, also search by codigo
            codigo_search = int(query)
            queryset = Insumo.objects.filter(Q(name__icontains=query) | Q(codigo=codigo_search))
        except ValueError:
            # If the query is not an int, just search by name
            queryset = Insumo.objects.filter(name__icontains=query)
    else:
        queryset = Insumo.objects.all().order_by('codigo')

    paginator = Paginator(queryset, 100)
    page_number = request.GET.get('page')
    insumos = paginator.get_page(page_number)

    start_page = insumos.number
    end_page = min(insumos.number + 4, insumos.paginator.num_pages)

    context = {
        'insumos': insumos,
        'start_page': start_page,
        'end_page': end_page,
    }

    return render(request, 'insumo_list.html', context)



def insumo_detail(request, codigo):
    insumo = get_object_or_404(Insumo, codigo=codigo)
    states = State.objects.all()
    related_compositions = CompositionInsumo.objects.filter(insumo=insumo).select_related('composition')

    state_costs = []

    for state in states:
        try:
            latest_desonerado_cost = CostHistory.objects.filter(
                insumo=insumo,
                state=state,
                cost_type=CostHistory.DESONERADO,
            ).latest('month_year')
        except CostHistory.DoesNotExist:
            latest_desonerado_cost = None

        try:
            latest_nao_desonerado_cost = CostHistory.objects.filter(
                insumo=insumo,
                state=state,
                cost_type=CostHistory.NAO_DESONERADO,
            ).latest('month_year')
        except CostHistory.DoesNotExist:
            latest_nao_desonerado_cost = None

        state_costs.append({
            'state': state,
            'latest_desonerado_cost': latest_desonerado_cost,
            'latest_nao_desonerado_cost': latest_nao_desonerado_cost,
        })

    context = {
        'insumo': insumo,
        'state_costs': state_costs,
        'related_compositions': related_compositions,
    }

    return render(request, 'compositions/insumo_detail.html', context)


def classe_detail(request, code):
    # Redirect to lowercase URL if the code is not lowercase
    if code != code.lower():
        return redirect('compositions:classe_detail', code=code.lower())

    # Try to get the classe using the uppercase version of the code
    classe = get_object_or_404(Classe, code=code.upper())
    
    grupos = classe.grupos.all().annotate(composition_count=Count('compositions'))
    
    context = {
        'classe': classe,
        'grupos': grupos,
    }
    
    return render(request, 'compositions/classe_detail.html', context)


def classes_list(request):
    # Query classes for each macrotema
    classes_01 = Classe.objects.filter(macrotema='01')
    classes_02 = Classe.objects.filter(macrotema='02')
    classes_03 = Classe.objects.filter(macrotema='03')

    # Render the list of classes using the template
    context = {
        'classes_01': classes_01,
        'classes_02': classes_02,
        'classes_03': classes_03,
    }
    return render(request, 'compositions/classes_list.html', context)


def composition_search_view(request):
    query = request.GET.get('q', '')
    if query:
        try:
            # Assuming Composition model has 'name' and 'codigo' fields like Insumo
            codigo_search = int(query)
            queryset = Composition.objects.filter(Q(name__icontains=query) | Q(codigo=codigo_search))
        except ValueError:
            queryset = get_relevant_queryset(Composition, query)
    else:
        queryset = Composition.objects.all().order_by('codigo')

    paginator = Paginator(queryset, 100)  # Adjust the pagination as needed
    page_number = request.GET.get('page')
    compositions = paginator.get_page(page_number)

    start_page = compositions.number
    end_page = min(compositions.number + 4, compositions.paginator.num_pages)

    context = {
        'compositions': compositions,
        'start_page': start_page,
        'end_page': end_page,
        'query': query,  # Add the query to the context for the form value
    }

    return render(request, 'compositions/composition_search.html', context)



def grupo_detail(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    compositions = grupo.compositions.all()  # Using the reverse relation
    
    context = {
        'grupo': grupo,
        'compositions': compositions,
    }
    
    return render(request, 'compositions/grupo_detail.html', context)




class CompositionViewSet(viewsets.ModelViewSet):
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer
    lookup_field = 'codigo'
    


def get_relevant_queryset(model, search_term):
    if not search_term:
        return model.objects.none()

    words = search_term.split()
    # Create Q objects for each word in the search term for icontains search.
    word_queries = [Q(name__icontains=word) for word in words]

    # Construct a single query that requires all words to match.
    all_words_query = Q()
    for query in word_queries:
        all_words_query &= query

    # Create the queryset filtering by the constructed all_words_query
    # Annotate with a boolean indicating if the name starts with the search term.
    queryset = model.objects.filter(all_words_query).annotate(
        starts_with_search=Case(
            When(name__istartswith=search_term, then=Value(True)),
            default=Value(False),
            output_field=IntegerField(),
        )
    ).order_by('-starts_with_search', 'name')  # Order by starts_with_search descending

    return queryset



class SearchCompositionView(APIView):

    def get_queryset(self):
        return Composition.objects.all()


    def get(self, request):
        codigo = request.GET.get('codigo')
        name = request.GET.get('name')
        
        if codigo and codigo != "[object Object]":
            compositions = Composition.objects.filter(codigo=codigo)

        # Handle search by name
        elif name:
            compositions = get_relevant_queryset(Composition, name)[:30]
            

        else:
            compositions = Composition.objects.none()
        
        serializer = CompositionSerializer(compositions, many=True)
        return Response(serializer.data)





class CompositionDetailView(APIView):

    queryset = Composition.objects.all()

    def get(self, request, codigo):
        composition = Composition.objects.filter(codigo=codigo).first()

        if composition:
                serializer = CompositionDetailSerializer(composition)
                return Response(serializer.data)
        else:
                return Response({"error": "Composição não encontrada"}, status=404)




class CompositionCostView(APIView):

    queryset = Composition.objects.all()

    def get_serializer_context(self):
        context = {
            'state': self.request.GET.get('state', None),
            'desonerado': self.request.GET.get('desonerado', None)
        }
        return context

    def get(self, request, codigo, state_name, desonerado):
        print(f"State in API view: {state_name}")  # Debugging line
        print(f"Desonerado in API view: {desonerado}")  # Debugging line
        # Get the State object using state_name
        state = get_object_or_404(State, name=state_name)

        composition = get_object_or_404(Composition, codigo=codigo)
        serializer_context = self.get_serializer_context()
        serializer = CompositionDetailSerializer(composition, context={'state': state, 'desonerado': desonerado})
        return Response(serializer.data)


class SearchInsumoView(APIView):

    def get_queryset(self):
        return Insumo.objects.all()


    def get(self, request):
        codigo = request.GET.get('codigo')
        name = request.GET.get('name')
        
        if codigo and codigo != "[object Object]":
            insumos = Insumo.objects.filter(codigo=codigo)

        # Handle search by name
        elif name:
            insumos = get_relevant_queryset(Insumo, name)[:30]
            

        else:
            insumos = Insumo.objects.none()
        
        serializer = InsumoSerializer(insumos, many=True)
        return Response(serializer.data)




class InsumoCostView(APIView):

    def get_queryset(self):
        return Insumo.objects.all()

    def get(self, request, codigo, state_name, desonerado):
        # Get the corresponding Insumo and State objects
        insumo = get_object_or_404(Insumo, codigo=codigo)
        state = get_object_or_404(State, name=state_name)

        # Get the latest cost
        try:
            latest_cost = CostHistory.objects.filter(
                insumo=insumo,
                state=state,
                cost_type=desonerado
            ).latest('month_year')
        except CostHistory.DoesNotExist:
            return Response({"error": "Cost history not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the data
        serializer = CostHistorySerializer(latest_cost)

        return Response(serializer.data)