import os
import json
import django
from django.db import transaction, IntegrityError
from datetime import date
import time 

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sinapi.settings')
django.setup()

from compositions.models import Insumo, CostHistory, State  # Importing the models

# Load JSON data
with open('data.json', 'r') as f:
    data = json.load(f)

# Define the date for October 2023
month_year = date(2023, 10, 1)
year_month = "202310"

# Atomic database transaction
with transaction.atomic():
    counter = 0  # Initialize a counter
    for codigo, state_data in data.items():
        counter += 1  # Increment the counter

        # Pause every 100 instances
        if counter % 500 == 0:
            print("Pausing for 3 seconds...")
            time.sleep(5)  # Pause for 3 seconds

        # Converting to str and removing leading/trailing whitespace
        codigo = str(codigo).strip()


        # Check if Insumo with this 'codigo' exists
        try:
            insumo_instance = Insumo.objects.get(codigo=codigo)
        except Insumo.DoesNotExist:
            print(f"No Insumo with codigo {codigo} found.")
            continue

        for state_cost_key, cost in state_data.items():
            state_name, cost_type_key = state_cost_key.split('_')

            # Normalize cost type to match the CostHistory model constants
            cost_type = CostHistory.NAO_DESONERADO if 'NaoDesonerado' in cost_type_key else CostHistory.DESONERADO

            # Get or create the State object
            state_instance, created = State.objects.get_or_create(name=state_name)

            try:
                # Create or update CostHistory
                cost_history_instance, created = CostHistory.objects.update_or_create(
                    insumo=insumo_instance,
                    state=state_instance,
                    month_year=month_year,
                    year_month=year_month,
                    cost_type=cost_type,
                    defaults={'cost': cost}
                )
            except IntegrityError as e:
                print(f"Skipped update_or_create for Insumo with codigo {codigo} due to IntegrityError: {e}")
                continue  # Skip to the next item

print("CostHistory has been updated.")
