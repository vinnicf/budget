import os
import django
from django.db import transaction

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sinapi.settings')
django.setup()

from compositions.models import Classe, Grupo  # Importing the required models
import json

# Load the JSON file
with open('output.json', 'r') as f:
    data = json.load(f)

# Keep track of unique pairs to avoid redundancy
unique_pairs = set()

with transaction.atomic():
    for entry in data:
        classe_code = entry["Classe"]
        grupo_name = entry["Grupo"]

        # Fetch the Classe based on the given code
        try:
            classe = Classe.objects.get(code=classe_code)
        except Classe.DoesNotExist:
            print(f"Classe {classe_code} does not exist. Skipping...")
            continue

        # To avoid redundant checks, see if this pair was already processed
        if (classe_code, grupo_name) in unique_pairs:
            continue

        # Check if the Grupo for this Classe exists or create a new one
        grupo, created = Grupo.objects.get_or_create(name=grupo_name, classe=classe)
        if created:
            print(f"Grupo {grupo_name} for Classe {classe_code} added.")

        # Mark this pair as processed
        unique_pairs.add((classe_code, grupo_name))

print("Import completed!")
