##Cache version of the cost_calculator method in the Composition


    cost_cache = {}

    def calculate_cost(self, state=None, desonerado=None):
        from compositions.models import CostHistory
        
        cache_key = f"{self.id}-{state}-{desonerado}"  # Create a unique key for each set of arguments

        # Check if the cost is already cached
        if cache_key in Composition.cost_cache:
            print("Cost retrieved from cache")
            return Composition.cost_cache[cache_key]

        print("In Calculate Cost")
        total_cost = 0

        if desonerado not in [CostHistory.DESONERADO, CostHistory.NAO_DESONERADO]:
            print(f"Invalid desonerado value: {desonerado}")
            return 0  # Or some other way to signal the error

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
                print(f"Custo unitário do insumo {comp_insumo.insumo.name}: {cost_history.cost}")
                print(f"Coeficiente para insumo {comp_insumo.insumo.codigo}: {comp_insumo.quantity}")
                individual_cost = Decimal(cost_history.cost) * Decimal(str(comp_insumo.quantity))
                individual_cost = individual_cost.quantize(Decimal('0.00'), rounding=ROUND_DOWN)  # Round down to 2 decimal places
                print(f"Custo calculado total para o insumo {comp_insumo.insumo.codigo}: {individual_cost}")
                total_cost += individual_cost

            else:
                print(f"No cost history found for insumo: {comp_insumo.insumo.codigo}")
            
            print(f"Quantity for insumo {comp_insumo.insumo.codigo}: {comp_insumo.quantity}")

        # Calculate cost for child compositions
        for comp_comp in self.compositionchild_set.all():
            child_composition_cost = comp_comp.child_composition.calculate_cost(state, desonerado)
            total_cost += child_composition_cost * comp_comp.quantity

        print(f"Total cost: {total_cost}")

        # Cache the total cost before returning it
        Composition.cost_cache[cache_key] = total_cost
        print("Cost stored in cache")

        total_cost = Decimal(total_cost).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
