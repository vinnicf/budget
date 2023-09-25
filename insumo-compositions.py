import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sinapi.settings')
django.setup()

from compositions.models import Insumo, Composition

def write_to_file(filename, data):
    with open(filename, 'w') as f:
        f.write(str(data))

def generate_files():
    # Fetch all 'codigo' values for Composition and Insumo
    compositions_codigos = [c.codigo for c in Composition.objects.all()]
    insumos_codigos = [i.codigo for i in Insumo.objects.all()]

    # Write to respective files
    write_to_file('compositions.txt', compositions_codigos)
    write_to_file('insumos.txt', insumos_codigos)

    print("Files generated successfully!")

generate_files()
