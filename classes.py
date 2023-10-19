import os
import django
import json
from django.db import transaction

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sinapi.settings')
django.setup()

from compositions.models import Grupo, Classe

# Path to your JSON file
json_file_path = 'output.json'

# Load the data from the JSON file
with open(json_file_path, 'r') as f:
    data = json.load(f)

with transaction.atomic():
    for key, value in data.items():
        # Split the key to get the classe_code and grupo_name
        classe_code, grupo_name = key.split('_')

        try:
            # Get the Grupo based on the provided name and its associated Classe code
            grupo = Grupo.objects.get(name=grupo_name, classe__code=classe_code)

            # Update the descricao of the Grupo
            grupo.descricao = value
            grupo.save()

            print(f"Grupo {grupo_name} of Classe {classe_code} updated with description {value}.")

        except Grupo.DoesNotExist:
            print(f"Grupo {grupo_name} of Classe {classe_code} does not exist. Skipping this item...")

print("Update complete!")
