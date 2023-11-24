from django.core.management.base import BaseCommand
from time import sleep
from compositions.models import Composition 

class Command(BaseCommand):
    help = 'List all unprocessed Composition instances'

    def handle(self, *args, **kwargs):
        unprocessed_compositions = Composition.objects.filter(comp_mo_cost=0, comp_material_cost=0)
        if unprocessed_compositions.exists():
            for comp in unprocessed_compositions:
                self.stdout.write(f"{comp.codigo} - {comp.name}")
        else:
            self.stdout.write(self.style.SUCCESS("All compositions have been processed."))