from django.db import models
from users.models import CustomUser

class Orcamento(models.Model):

    DESONERADO_CHOICES = [
        ('desonerado', 'Desonerado'),
        ('nao_desonerado', 'Não Desonerado'),
    ]

    name = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    bdi = models.DecimalField(max_digits=5, decimal_places=2)
    desonerado = models.CharField(max_length=15, choices=DESONERADO_CHOICES, default='nao_desonerado')
    state = models.CharField(max_length=2)
    
    # A string representation for the model
    def __str__(self):
        return self.name

class OrcamentoItem(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='items')
    refid = models.CharField(max_length=10)
    itemtype = models.CharField(max_length=10)
    subtype = models.CharField(max_length=10, blank=True, null=True)
    codigo = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=255)
    unit = models.CharField(max_length=5, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mo_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    material_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    # A string representation for the model
    def __str__(self):
        return f"{self.description} - {self.orcamento.name}"