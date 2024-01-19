

    example_items = [
        {'refid': '001', 'codigo': '38464', 'itemtype': 'subitem', 'unit': 'M3', 'quantity': 100, unit,, 'description': 'CONCRETO USINADO BOMBEAVEL, CLASSE DE RESISTENCIA C20, COM BRITA 0, SLUMP = 220 +/- 20 MM, COM BOMBEAMENTO (DISPONIBILIZACAO DE BOMBA), SEM O LANCAMENTO (NBR 8953)', ...},  # Fill in the details
        
        # Add more items as needed
    ]



def create_example_budget(user):
    # Create an example Orcamento
    example_orcamento = Orcamento.objects.create(
        name="Example Budget",
        user=user,
        bdi=0.1,  # Example value
        desonerado='nao_desonerado',
        state='SP',
        datasinapi="202311"  # Example value
    )

    # Create OrcamentoItems for the example Orcamento


    for item in example_items:
        OrcamentoItem.objects.create(orcamento=example_orcamento, **item)
