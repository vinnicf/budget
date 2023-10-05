from django.shortcuts import render, get_object_or_404
from .models import Composition, CostHistory
from rest_framework import viewsets, status
from .serializers import CompositionSerializer, CompositionDetailSerializer
from django.db.models import Q, Count, F, ExpressionWrapper, fields, Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response




def composition_detail(request, codigo):
    composition = get_object_or_404(Composition, codigo=codigo)
    return render(request, 'compositions/composition_detail.html', {'composition': composition})


def composition_list(request):
    compositions = Composition.objects.all()

    for composition in compositions:
        composition.num_children = composition.compositionchild_set.count()
        composition.num_insumos = composition.compositioninsumo_set.count()
        composition.total_children = composition.num_children + composition.num_insumos

    return render(request, 'compositions/composition_list.html', {'compositions': compositions})






class CompositionViewSet(viewsets.ModelViewSet):
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer
    lookup_field = 'codigo'
    

class SearchCompositionView(APIView):

    def get_queryset(self):
        return Composition.objects.all()


    def get(self, request):
        codigo = request.GET.get('codigo')
        name = request.GET.get('name')
        
        if codigo and codigo != "[object Object]":
            compositions = Composition.objects.filter(codigo=codigo)
        elif name:
            compositions = Composition.objects.filter(name__icontains=name)[:30]
        else:
            compositions = Composition.objects.none()

        print("Filtered Compositions:", compositions)  

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
                return Response({"error": "Composition not found"}, status=404)

