from django.core.management.base import BaseCommand, CommandError
from compositions.models import CostHistory

class Command(BaseCommand):
    help = 'Populate the year_month_str field in CostHistory'

    def add_arguments(self, parser):
        # Optional arguments
        parser.add_argument('--start_id', type=int, help='Start of the ID range')
        parser.add_argument('--end_id', type=int, help='End of the ID range')

    def handle(self, *args, **options):
        start_id = options['start_id'] or 0
        end_id = options['end_id'] or CostHistory.objects.latest('id').id

        if start_id > end_id:
            raise CommandError('Start ID must be less than or equal to End ID')

        for cost_history in CostHistory.objects.filter(id__range=(start_id, end_id)):
            cost_history.year_month = cost_history.month_year.strftime('%Y%m')
            cost_history.save()
