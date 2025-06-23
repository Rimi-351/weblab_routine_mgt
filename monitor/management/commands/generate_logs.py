import re
from django.core.management.base import BaseCommand
from routine.models import Routine
from monitor.models import DailyClassLog
from teachers.models import Reschedule
from courses.models import Course
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Generate class logs for today or the full week'

    def add_arguments(self, parser):
        parser.add_argument(
            '--week',
            action='store_true',
            help='Generate logs for the full week (7 days)',
        )

    def handle(self, *args, **options):
        if options['week']:
            for offset in range(7):
                target_date = date.today() + timedelta(days=offset)
                self.generate_logs_for_date(target_date)
            self.stdout.write(self.style.SUCCESS("✅ Weekly class logs generated successfully."))
        else:
            self.generate_logs_for_date(date.today())
            self.stdout.write(self.style.SUCCESS("✅ Today's class logs generated successfully."))

    def extract_course_number(self, course_str):
        # Defensive cleaning and extraction
        if not course_str:
            return None
        # Remove prefix like '3 : ' if exists
        if ':' in course_str:
            course_str = course_str.split(':', 1)[1].strip()

        # Extract the course code part before ' - '
        parts = course_str.split(' - ')
        if not parts:
            return None
        code_part = parts[0]

        # Extract numeric part from code_part
        match = re.search(r'\d+', code_part)
        if match:
            return match.group(0)
        return None

    def generate_logs_for_date(self, target_date):
        weekday = target_date.strftime('%A')
        self.stdout.write(f"Generating logs for {target_date} ({weekday})")

        # Step 1: Build rescheduled signatures (teacher_id, course_number)
        reschedules = Reschedule.objects.filter(class_schedule__original_date=target_date)
        self.stdout.write(f"original date {target_date} ({weekday})")
        rescheduled_signatures = set()

        for r in reschedules:
            course_num = self.extract_course_number(r.class_schedule.subject)
            if not course_num:
                self.stdout.write(self.style.WARNING(
                    f"⚠️ Couldn't extract course number from rescheduled subject: '{r.class_schedule.subject}'"
       
                ))
            sig = (r.class_schedule.teacher_id, course_num)
            rescheduled_signatures.add(sig)

        self.stdout.write("\n📌 Rescheduled Signatures:")
        for sig in rescheduled_signatures:
            self.stdout.write(f"  🔁 {sig}")

        # Step 2: Process routine classes
        routines = Routine.objects.filter(slot__day=weekday)
        self.stdout.write("\n📌 Routine Signatures:")
        for r in routines:
            course_num = self.extract_course_number(f"{r.course.code} - {r.course.title}")
            sig = (r.teacher.id, course_num)
            self.stdout.write(f"  📘 {sig}")

            if sig in rescheduled_signatures:
                self.stdout.write(f"    ❌ Skipping rescheduled: {sig}")
                continue

            DailyClassLog.objects.get_or_create(
                course=r.course,
                teacher=r.teacher,
                date=target_date,
                start_time=r.slot.start_time,
                end_time=r.slot.end_time,
                semester=r.batch,
                defaults={'status': 'pending'}
            )
            self.stdout.write(f"    ✅ Added routine class log: {sig}")

        # Step 3: Add rescheduled classes
        reschedules_today = Reschedule.objects.filter(reschedule_date=target_date)
        for r in reschedules_today:
            course_code = r.class_schedule.subject.split(" - ")[0]
            try:
                course = Course.objects.get(code=course_code)
            except Course.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"❌ Course with code '{course_code}' not found for reschedule"))
                continue
            DailyClassLog.objects.filter(
                course=course,
                teacher=r.class_schedule.teacher,
                date=r.class_schedule.original_date or r.class_schedule.date,
                start_time=r.class_schedule.start_time,
                end_time=r.class_schedule.end_time,
            ).delete()

            DailyClassLog.objects.get_or_create(
                course=course,
                teacher=r.class_schedule.teacher,
                date=r.reschedule_date,
                start_time=r.new_start_time or r.class_schedule.start_time,
                end_time=r.new_end_time or r.class_schedule.end_time,
                semester='3-2',  # fallback
                defaults={'status': 'rescheduled'}
            )
            self.stdout.write(f"    🔁 Added rescheduled class log: {course_code}")



