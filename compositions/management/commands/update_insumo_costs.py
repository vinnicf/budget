from django.core.management.base import BaseCommand
from compositions.models import Insumo 

class Command(BaseCommand):
    help = 'Updates current cost for all Insumo instances and marks inactive if current cost is 0'

    def handle(self, *args, **kwargs):
        for insumo in Insumo.objects.all():
            insumo.update_current_cost()

            # Check if currentcost is 0 and mark as inactive
            if insumo.currentcost == 0:
                insumo.inativo = True
                insumo.save()
                self.stdout.write(self.style.WARNING(f'{insumo.name} marked as inactive due to zero cost.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated cost for {insumo.name}'))