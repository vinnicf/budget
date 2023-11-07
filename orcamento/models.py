from django.db import models


class Orcamento(models.Model):

    DESONERADO_CHOICES = [
        ('desonerado', 'Desonerado'),
        ('nao_desonerado', 'Não Desonerado'),
    ]

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    bdi = models.DecimalField(max_digits=5, decimal_places=2)
    desonerado = models.CharField(max_length=15, choices=DESONERADO_CHOICES, default='nao_desonerado')
    state = models.CharField(max_length=2)
    
    
    # A string representation for the model
    def __str__(self):
        return self.name

class OrcamentoItem(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='items')
    refid = models.Charfield(max_length=10)
    itemtype = models.CharField(max_lenght=10)
    codigo = models.CharField(max_lenght=10)
    description = models.CharField(max_length=255)
    unit = models.Charfield(max_lenght=5)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    mo_cost = models.DecimalField(max_digits=10, decimal_places=2)
    material_cost = models.DecimalField(max_digits=10, decimal_places=2)

    

    # A string representation for the model
    def __str__(self):
        return f"{self.description} - {self.orcamento.name}"