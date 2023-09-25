from django.db import models


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Insumo(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Composition(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)
    # Here we have a ManyToMany relationship with a through model to capture quantity
    insumos = models.ManyToManyField(Insumo, through='CompositionInsumo')
    compositions = models.ManyToManyField(
        'self', symmetrical=False, through='CompositionComposition', related_name='child_compositions')

    def __str__(self):
        return self.name


class CompositionInsumo(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.insumo.name} in {self.composition.name}"


class CompositionComposition(models.Model):
    parent_composition = models.ForeignKey(
        Composition, on_delete=models.CASCADE, related_name='parent_composition_set')
    child_composition = models.ForeignKey(
        Composition, on_delete=models.CASCADE, related_name='child_composition_set')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

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
