from django.db import models


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Insumo(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)
    currentcost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Decimal field for cost

    def __str__(self):
        return self.name


class Composition(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)
    # Here we have a ManyToMany relationship with a through model to capture quantity
    insumos = models.ManyToManyField(Insumo, through='CompositionInsumo')
    compositions = models.ManyToManyField(
        'self', symmetrical=False, through='CompositionComposition', related_name='parent_compositions')



    def calculate_cost(self):
        total_cost = 0
        for comp_insumo in self.compositioninsumo_set.all():
            total_cost += comp_insumo.insumo.currentcost * comp_insumo.quantity

        for comp_comp in self.compositionchild_set.all():
            total_cost += comp_comp.child_composition.calculate_cost() * comp_comp.quantity

        return total_cost

    def total_cost(self):
        return self.calculate_cost()

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
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    month_year = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ["insumo", "state", "month_year"]
        indexes = [
            models.Index(fields=["insumo", "state", "month_year"]),
        ]

    def __str__(self):
        return f"{self.insumo.name} cost in {self.state.name} for {self.month_year.strftime('%B %Y')}"
