from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from compositions.models import Classe, Grupo, Insumo, Composition

class ClasseSitemap(Sitemap):
    def items(self):
        return Classe.objects.all()

    def location(self, obj):
        return reverse('compositions:classe_detail', args=[obj.code])

class GrupoSitemap(Sitemap):
    def items(self):
        return Grupo.objects.all()

    def location(self, obj):
        return reverse('compositions:grupo_detail', args=[obj.id])

class InsumoSitemap(Sitemap):
    def items(self):
        return Insumo.objects.all()

    def location(self, obj):
        return reverse('compositions:insumo_detail', args=[obj.codigo])

class CompositionSitemap(Sitemap):
    def items(self):
        return Composition.objects.all()

    def location(self, obj):
        return reverse('compositions:composition_detail', args=[obj.codigo])
