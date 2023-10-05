import os
import json
import django
from django.db import transaction
from datetime import date
from calendar import monthrange

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sinapi.settings')
django.setup()

from compositions.models import Insumo, CostHistory, State  # Importing the models

# Load JSON data
with open('output.json', 'r') as f:
    data = json.load(f)

# Get or create the State object for RS
state_instance, created = State.objects.get_or_create(name='RS')

# Define the date for August 2023
month_year = date(2023, 8, 1)

# Atomic database transaction
with transaction.atomic():
    for item in data:
        codigo = str(item.get('CODIGO  ')).strip()  # Converting to str and removing leading/trailing whitespace
        nao_desonerado = item.get('NAO DESONERADO')
        desonerado = item.get('DESONERADO')

        # Check if Insumo with this 'codigo' exists
        try:
            insumo_instance = Insumo.objects.get(codigo=codigo)
        except Insumo.DoesNotExist:
            print(f"No Insumo with codigo {codigo} found.")
            continue

        # Create or update CostHistory for nao_desonerado
        cost_history_instance, created = CostHistory.objects.update_or_create(
            insumo=insumo_instance,
            state=state_instance,
            month_year=month_year,
            cost_type=CostHistory.NAO_DESONERADO,
            defaults={'cost': nao_desonerado}
        )
        print(f"Updated CostHistory for {cost_history_instance}")

        # Create or update CostHistory for desonerado
        cost_history_instance, created = CostHistory.objects.update_or_create(
            insumo=insumo_instance,
            state=state_instance,
            month_year=month_year,
            cost_type=CostHistory.DESONERADO,
            defaults={'cost': desonerado}
        )
        print(f"Updated CostHistory for {cost_history_instance}")

print("CostHistory has been updated.")
