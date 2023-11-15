from django.core.management.base import BaseCommand
from compositions.models import Insumo 

class Command(BaseCommand):
    help = 'Updates current cost for all Insumo instances'

    def handle(self, *args, **kwargs):
        for insumo in Insumo.objects.all():
            insumo.update_current_cost()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated cost for {insumo.name}'))
