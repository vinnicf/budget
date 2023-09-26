from django.shortcuts import render, get_object_or_404
from .models import Composition

def composition_detail(request, codigo):
    composition = get_object_or_404(Composition, codigo=codigo)
    return render(request, 'compositions/composition_detail.html', {'composition': composition})


def composition_list(request):
    compositions = Composition.objects.all()
    return render(request, 'compositions/composition_list.html', {'compositions': compositions})
