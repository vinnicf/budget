from django.db import models
from calendar import monthrange
import math
from decimal import Decimal, ROUND_DOWN

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Classe(models.Model):
    CHOICES = [
        ('01', 'Habitação, Fundações e Estruturas'),
        ('02', 'Instalações Hidráulicas e Elétricas Prediais e Redes de Distribuição de Energia Elétrica'),
        ('03', 'Saneamento e Infraestrutura Urbana'),
    ]

    macrotema = models.CharField(
        max_length=2,
        choices=CHOICES,
        default='01',  # Optional default
    )
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.code

class Grupo(models.Model):
    name = models.CharField(max_length=10)
    classe = models.ForeignKey(Classe, related_name='grupos', on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Insumo(models.Model):
    MATERIAL = 'MATERIAL'
    MO = 'MO'

    TYPE_CHOICES = [
        (MATERIAL, 'Material'),
        (MO, 'Mão de Obra'),
    ]

    codigo = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)
    currentcost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    insumo_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=MATERIAL,
    )
    detaileddescription = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name

class Composition(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=400)
    unit = models.CharField(max_length=10)
    comp_cost = models.DecimalField(max_digits=25, decimal_places=2, default=0.00, editable=False)
    # Here we have a ManyToMany relationship with a through model to capture quantity
    insumos = models.ManyToManyField(Insumo, through='CompositionInsumo')
    compositions = models.ManyToManyField(
        'self', symmetrical=False, through='CompositionComposition', related_name='parent_compositions')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='compositions', null=True)

    # Fields for caderno tecnico
    ct_itens = models.TextField(null=True, blank=True)
    ct_equipamento = models.TextField(null=True, blank=True)
    ct_quantificacao = models.TextField(null=True, blank=True)
    ct_afericao = models.TextField(null=True, blank=True)
    ct_execucao = models.TextField(null=True, blank=True)
    ct_complementares = models.TextField(null=True, blank=True)

  
    def calculate_cost(self, state=None, desonerado=None):
        from compositions.models import CostHistory
    
        print("In Calculate Cost")
        total_cost = Decimal('0.00')
        material_cost = Decimal('0.00')
        mo_cost = Decimal('0.00')

        if desonerado not in [CostHistory.DESONERADO, CostHistory.NAO_DESONERADO]:
            print(f"Invalid desonerado value: {desonerado}")
            return total_cost, mo_cost

        # Calculate cost for insumos in this composition
        for comp_insumo in self.compositioninsumo_set.all():
            print(f"Checking insumo: {comp_insumo.insumo.codigo}")
            print(f"Filtering cost_history with desonerado value: {desonerado}")
            cost_history = CostHistory.objects.filter(
                insumo=comp_insumo.insumo,
                state=state,
                cost_type=desonerado
            ).last()

            if cost_history:
                individual_cost = Decimal(cost_history.cost) * Decimal(str(comp_insumo.quantity))
                individual_cost = individual_cost.quantize(Decimal('0.00'), rounding=ROUND_DOWN)  # Round down to 2 decimal places
                print(f"Custo calculado total para o insumo {comp_insumo.insumo.codigo}: {individual_cost}")
                total_cost += individual_cost

                # Categorize costs based on the type of Insumo
                if comp_insumo.insumo.insumo_type == Insumo.MO:
                    mo_cost += individual_cost

            else:
                print(f"No cost history found for insumo: {comp_insumo.insumo.codigo}")
            
            print(f"Quantity for insumo {comp_insumo.insumo.codigo}: {comp_insumo.quantity}")

        # Calculate cost for child compositions
        for comp_comp in self.compositionchild_set.all():
            child_composition_cost, child_material_cost, child_mo_cost = comp_comp.child_composition.calculate_cost(state, desonerado)
            child_composition_total_cost = child_composition_cost * comp_comp.quantity
            child_composition_total_cost = child_composition_total_cost.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
            total_cost += child_composition_total_cost
            mo_cost += (child_mo_cost * comp_comp.quantity).quantize(Decimal('0.00'), rounding=ROUND_DOWN)

        print(f"Total cost: {total_cost}")
        print(f"MO cost: {mo_cost}")

       

        total_cost = total_cost.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        mo_cost = mo_cost.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        material_cost = total_cost - mo_cost

        return total_cost, material_cost, mo_cost


    def __str__(self):
        return self.name




class CompositionInsumo(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=25, decimal_places=10, null=True)

    def __str__(self):
        return f"{self.insumo.name} in {self.composition.name}"


class CompositionComposition(models.Model):
    parent_composition = models.ForeignKey(
        Composition, on_delete=models.CASCADE, related_name='compositionchild_set')
    child_composition = models.ForeignKey(
        Composition, on_delete=models.CASCADE, related_name='compositionparent_set')
    quantity = models.DecimalField(max_digits=25, decimal_places=10, null=True)

    def __str__(self):
        return f"{self.child_composition.name} in {self.parent_composition.name}"


class CostHistory(models.Model):
    DESONERADO = 'desonerado'
    NAO_DESONERADO = 'nao_desonerado'
    COST_TYPE_CHOICES = [
        (DESONERADO, 'Desonerado'),
        (NAO_DESONERADO, 'Não Desonerado'),
    ]
    
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    month_year = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    cost_type = models.CharField(
        max_length=15, 
        choices=COST_TYPE_CHOICES,
        default=NAO_DESONERADO
    )

    class Meta:
        unique_together = ["insumo", "state", "month_year", "cost_type"]
        indexes = [
            models.Index(fields=["insumo", "state", "month_year", "cost_type"]),
        ]

    def __str__(self):
        return f"{self.insumo.name} ({self.get_cost_type_display()}) cost in {self.state.name} for {self.month_year.strftime('%B %Y')}"

    def save(self, *args, **kwargs):
        last_day_of_month = monthrange(self.month_year.year, self.month_year.month)[1]
        self.month_year = self.month_year.replace(day=last_day_of_month)
        super().save(*args, **kwargs)








