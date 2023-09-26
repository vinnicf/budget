from django.shortcuts import render, get_object_or_404
from .models import Composition
from rest_framework import viewsets
from .serializers import CompositionSerializer

def composition_detail(request, codigo):
    composition = get_object_or_404(Composition, codigo=codigo)
    return render(request, 'compositions/composition_detail.html', {'composition': composition})


def composition_list(request):
    compositions = Composition.objects.all()
    return render(request, 'compositions/composition_list.html', {'compositions': compositions})



class CompositionViewSet(viewsets.ModelViewSet):
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer
    lookup_field = 'codigo'
