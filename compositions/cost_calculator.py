    def calculate_cost(self, state=None, desonerado=None):
        from compositions.models import CostHistory
    
        print("In Calculate Cost")
        total_cost = Decimal('0.00')
        material_cost = Decimal('0.00')
        mo_cost = Decimal('0.00')

        if desonerado not in [CostHistory.DESONERADO, CostHistory.NAO_DESONERADO]:
            print(f"Invalid desonerado value: {desonerado}")
            return total_cost, material_cost, mo_cost

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

                # Categorize costs based on the type of Insumo
                if comp_insumo.insumo.insumo_type == Insumo.MATERIAL:
                    material_cost += individual_cost
                elif comp_insumo.insumo.insumo_type == Insumo.MO:
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

            material_cost += (child_material_cost * comp_comp.quantity).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
            mo_cost += (child_mo_cost * comp_comp.quantity).quantize(Decimal('0.00'), rounding=ROUND_DOWN)

        print(f"Total cost: {total_cost}")
        print(f"Material cost: {material_cost}")
        print(f"MO cost: {mo_cost}")

       

        total_cost = total_cost.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        material_cost = material_cost.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        mo_cost = mo_cost.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

        return total_cost, material_cost, mo_cost

