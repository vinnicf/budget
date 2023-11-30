from django.core.management.base import BaseCommand
from compositions.models import CostHistory

class Command(BaseCommand):
    help = 'Populate the year_month_str field in CostHistory'

    def handle(self, *args, **kwargs):
        for cost_history in CostHistory.objects.filter(id__gt=425000):
            cost_history.year_month = cost_history.month_year.strftime('%Y%m')
            cost_history.save()
