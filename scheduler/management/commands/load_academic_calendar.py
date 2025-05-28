import os
import pandas as pd
from django.core.management.base import BaseCommand
from scheduler.models import AcademicCalendar  # Replace with your actual model

class Command(BaseCommand):
    help = 'Load academic calendar data from Excel file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(__file__), 'academic_calendar.xlsx')

        try:
            df = pd.read_excel(file_path)

            # Loop through rows
            for _, row in df.iterrows():
                date = row['date']
                event_name = row['event_name']  # or whatever your column is called

                AcademicCalendar.objects.create(date=date, event_name=event_name)

            self.stdout.write(self.style.SUCCESS('Successfully loaded academic calendar.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading academic calendar: {e}'))
