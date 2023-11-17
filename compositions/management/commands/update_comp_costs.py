from django.core.management.base import BaseCommand
from time import sleep
from compositions.models import Composition 

class Command(BaseCommand):
    help = 'Updates current cost for Composition instances within a specified codigo range'

    def add_arguments(self, parser):
        # Add arguments to command
        parser.add_argument('start_codigo', type=str, help='Starting codigo for range')
        parser.add_argument('end_codigo', type=str, help='Ending codigo for range')

    def handle(self, *args, **kwargs):
        start_codigo = kwargs['start_codigo']
        end_codigo = kwargs['end_codigo']

        compositions = Composition.objects.filter(codigo__gte=start_codigo, codigo__lte=end_codigo)
        total = compositions.count()
        self.stdout.write(f"Starting the update process for compositions with codigo from {start_codigo} to {end_codigo} (total {total}).")

        sleep(5)

        for index, composition in enumerate(compositions, start=1):
            composition.update_composition_costs()
            self.stdout.write(self.style.SUCCESS(f'Updated cost for {composition.name} ({index}/{total})'))

            # Introduce a delay to reduce server load
            sleep(2)  # 2 second delay;

        self.stdout.write(self.style.SUCCESS("Selected composition costs updated successfully."))