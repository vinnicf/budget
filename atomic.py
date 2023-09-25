import os
import django
import openpyxl
from decimal import Decimal
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sinapi.settings')
django.setup()

from compositions.models import Insumo, Composition, CompositionInsumo, CompositionComposition



def read_codigos_from_file(filename):
    with open(filename, 'r') as file:
        codigos = eval(file.read())  # Read the list from the file
    return codigos


existing_compositions_codigos = read_codigos_from_file('compositions.txt')
existing_insumos_codigos = read_codigos_from_file('insumos.txt')

def import_compositions_from_xlsx(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    added_count = 0
    current_row = 2  # Starting from the second row after headers

    with transaction.atomic():
        while current_row <= sheet.max_row:
            row = [cell.value for cell in sheet[current_row]]

            label = row[0]
            codigo = row[1]
            name = row[2]
            unit = row[3]
            amount = row[4]

            if label not in ["COMPOSICAO", "INSUMO"]:
                # Check if this parent composition already exists
                if codigo not in existing_compositions_codigos:

                    children_complete = True  # Assuming initially that all children exist

                    # Check child compositions
                    child_row_idx = current_row + 1
                    while child_row_idx <= sheet.max_row:
                        child_row = [cell.value for cell in sheet[child_row_idx]]
                        child_label = child_row[0]
                        
                        if child_label in ["COMPOSICAO", "INSUMO"]:
                            child_codigo = child_row[1]
                            if child_label == "COMPOSICAO" and child_codigo not in existing_compositions_codigos:
                                children_complete = False
                                break
                            elif child_label == "INSUMO" and child_codigo not in existing_insumos_codigos:
                                children_complete = False
                                break
                            child_row_idx += 1
                        else:
                            break  # Reached another parent, break the loop

                    if children_complete:
                        parent_composition = Composition.objects.create(codigo=codigo, name=name, unit=unit)

                        # Add child compositions and insumos
                        for child_row_iter in range(current_row + 1, child_row_idx):
                            child_row = [cell.value for cell in sheet[child_row_iter]]
                            child_label = child_row[0]
                            child_codigo = child_row[1]
                            child_amount = child_row[4]
                            if child_label == "COMPOSICAO":
                                child_composition = Composition.objects.get(codigo=child_codigo)
                                CompositionComposition.objects.create(parent_composition=parent_composition,
                                                                     child_composition=child_composition,
                                                                     quantity=child_amount)
                            else:
                                child_insumo = Insumo.objects.get(codigo=child_codigo)
                                CompositionInsumo.objects.create(composition=parent_composition,
                                                                 insumo=child_insumo,
                                                                 quantity=child_amount)

                        print(f"Successfully added Composition: {name} (Codigo: {codigo})")
                        added_count += 1
                        if added_count >= 10:
                            break

            current_row += 1

    wb.close()

import_compositions_from_xlsx("compositions-v2.xlsx")




