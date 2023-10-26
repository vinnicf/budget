from django.http import JsonResponse, HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, NamedStyle
from openpyxl.utils import get_column_letter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from io import BytesIO
import math


@api_view(['POST'])
@permission_classes([AllowAny])
def export_excel(request):
    print("Request Data: ", request.data)  # Debug line
    items = request.data.get('items', [])
    BDI = request.data.get('BDI', 0.1)  # Default value can be set here if needed
    name = request.data.get('name', '')  # Default value can be set here if needed
    desonerado = request.data.get('desonerado', 'nao_desonerado')  # Default value can be set here if needed
    print("BDI Value: ", BDI)  # Debug line
    

    wb = Workbook()
    ws = wb.active

    arial_font = Font(name='Arial', size=10)
    number_style = NamedStyle(name='number_style', number_format="#,##0.00")

    # Add header
    headers = ['Item', 'Código', 'Descrição', 'Unidade', 'Qtd', 'Custo Unit', 'Preço Unit MO', 'Preço Unit Material', 'Preço Unit Total', 'Total MO', 'Total Material', 'Total']
   
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        ws['{}4'.format(col_letter)] = header
        ws['{}4'.format(col_letter)].alignment = Alignment(horizontal='center')


    # Styling
    for row_num in range(1, 4):
        ws.row_dimensions[row_num].height = 25

    ws.column_dimensions['C'].width = 64
    
    row_num = 5  # Start adding budget data from row 5

    bold_font = Font(bold=True, name='Arial')
    center_alignment = Alignment(horizontal='center')


    # Additional headers and meta-info
    ws['C1'] = 'Obra'
    ws['C1'].font = Font(name='Arial', size=10, bold=True)
    ws['C2'] = 'Projeto de Instalações Elétricas - UBS Moura'

    ws['E1'] = 'Bancos'
    ws['E1'].font = Font(name='Arial', size=10, bold=True)
    ws['E2'] = 'SINAPI - 08/2023'

    ws['H1'] = 'B.D.I.'
    ws['H1'].font = Font(name='Arial', size=10, bold=True)
    ws['H2'] = "22.0%"  # Example BDI

    ws['K1'] = 'Encargos Sociais'
    ws['K2'].font = Font(name='Arial', size=10, bold=True)
    ws['K2'] = 'Não Desonerado'

    # Merge and Center Cell for Row 3
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=len(headers))
    centered = Alignment(horizontal='center', vertical='center')
    ws['A3'].alignment = centered
    ws['A3'].value = "Planilha Orçamentária"
    ws['A3'].font = Font(name='Arial', size=10, bold=True)

    # Set height for row 2
    ws.row_dimensions[2].height = 60


    for item in items:

        if item.get('type') == 'stage':
            # Only include 'refId' and 'name' for stage rows
            refId = item.get('refId', '').upper()
            name = item.get('name', '').upper()
            row = [refId, '', name]
            for i in range(len(row), len(headers)):
                row.append('')  # Fill the remaining columns with empty strings

        else:
            refId = item.get('refId', '')
            codigo = item.get('codigo', '')
            name = item.get('name', '')
            unit = item.get('unit', '')
            quantity = item.get('quantity', 0)
            total_cost = item.get('total_cost', 0)
            mo_cost = item.get('mo_cost', 0)
            material_cost = item.get('material_cost', 0)
            costWithBDI = item.get('costWithBDI', 0)

            preco_unit_mo = math.floor(mo_cost * (1 + BDI) * 100) / 100.0
            preco_unit_material = math.floor(material_cost * (1 + BDI) * 100) / 100.0
            preco_unit_total = preco_unit_material + preco_unit_mo
            total_mo = preco_unit_mo * quantity
            total_material = preco_unit_material * quantity
            total = preco_unit_total * quantity

            row = [refId, codigo, name, unit, quantity, total_cost, preco_unit_mo, preco_unit_material, preco_unit_total, total_mo, total_material, total]
            
        ws.append(row)

        for col_num in range(1, len(headers) + 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.font = arial_font
            
            # Center-align all columns except 'Name/Description'
            if col_num != 3:
                cell.alignment = center_alignment

            if col_num in [6, 7, 8, 9, 10, 11, 12]:
                 cell.number_format = "#,##0.00"



        # Set height for all rows
        ws.row_dimensions[row_num].height = 35

         # Wrap text for the 3rd column (Name/Description)
        cell_to_wrap = ws.cell(row=row_num, column=3)
        cell_to_wrap.alignment = Alignment(wrap_text=True)

        if item.get('type') == 'stage':
            fill = PatternFill(start_color='DDEBF7',
                               end_color='DDEBF7', fill_type='solid')
            for col in range(1, len(row) + 1):
                cell = ws.cell(row=row_num, column=col)
                cell.fill = fill
                cell.font = bold_font  # Make the text bold for stage rows
        
        row_num += 1

    # Save it to a BytesIO object
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    # Create the HttpResponse
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Budget.xlsx'
    return response