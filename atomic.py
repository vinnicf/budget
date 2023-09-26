import openpyxl
import json

def xlsx_to_json(file_path, output_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    compositions = {}
    current_parent = None

    for row in sheet.iter_rows(min_row=2, values_only=True):  # Start from the second row to skip header
        if row[0] not in ["COMPOSICAO", "INSUMO"]:
            # This is a parent composition
            current_parent = row[1]  # Assuming codigo is in column 1
            compositions[current_parent] = {
                "codigo": current_parent,
                "name": row[2],
                "unit": row[3],
                "children": []
            }
        else:
            # These are children
            if current_parent:
                child = {
                    "type": row[0],
                    "codigo": row[1],
                    "name": row[2],
                    "unit": row[3],
                    "quantity": row[4]
                }
                compositions[current_parent]["children"].append(child)

    wb.close()

    with open(output_path, 'w') as outfile:
        json.dump(list(compositions.values()), outfile)

# Execute the function
xlsx_to_json("compositions-v2.xlsx", "transformed_data.json")
