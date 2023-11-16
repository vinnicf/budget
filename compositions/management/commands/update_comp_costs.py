from django.core.management.base import BaseCommand
from time import sleep
from compositions.models import Composition 

class Command(BaseCommand):
    help = 'Updates current cost for all Composition instances'

    def handle(self, *args, **kwargs):
        compositions = Composition.objects.all()
        total = compositions.count()
        self.stdout.write(f"Starting the update process for {total} compositions.")

        for index, composition in enumerate(compositions, start=1):
            composition.update_composition_costs()
            self.stdout.write(self.style.SUCCESS(f'Updated cost for {composition.codigo} - {composition.name} ({index}/{total})'))

            # Introduce a delay to reduce server load
            sleep(2)  

        self.stdout.write(self.style.SUCCESS("All composition costs updated successfully."))