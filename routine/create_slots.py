from django.core.management.base import BaseCommand
from routine.models import Slot
from datetime import datetime

class Command(BaseCommand):
    help = 'Creates time slots'

    def handle(self, *args, **options):
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
        
        time_ranges = [
            ('09:00', '10:20'),
            ('10:25', '11:45'),
            ('10:25', '13:10'),
            ('11:50', '13:10'),
            ('14:00', '15:20'),
            ('14:00', '16:45'),
            ('15:25', '16:45'),
        ]
        
        for day in days:
            for start_str, end_str in time_ranges:
                start_time = datetime.strptime(start_str, '%H:%M').time()
                end_time = datetime.strptime(end_str, '%H:%M').time()
                
                slot, created = Slot.objects.get_or_create(
                    day=day,
                    start_time=start_time,
                    end_time=end_time,
                    defaults={'is_available': True}
                )
                if created:
                    self.stdout.write(f"Created slot: {slot}")
                else:
                    self.stdout.write(f"Slot already exists: {slot}")