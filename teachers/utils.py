# def generate_class_schedule(start_date, end_date):
#             day_name_to_num = {
#                 'Monday': 0, 'Tuesday': 1, 'Wednesday': 2,
#                 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6,
#             }
#             routines = Routine.objects.all()
#             vacation_dates = []  # You can fetch from model later

#             deleted_count, _ = ClassSchedule.objects.filter(date__range=(start_date, end_date)).delete()

#             created_count = 0
#             skipped_conflicts = 0
#             current_date = start_date
#             while current_date <= end_date:
#                 if current_date in vacation_dates:
#                     current_date += timedelta(days=1)
#                     continue

#                 weekday_num = current_date.weekday()

#                 for routine in routines:
#                     if day_name_to_num.get(routine.slot.day) == weekday_num:
#                         if ClassSchedule.objects.filter(
#                             room=routine.room,
#                             date=current_date,
#                             start_time=routine.slot.start_time
#                         ).exists():
#                             skipped_conflicts += 1
#                             continue

#                         try:
#                             ClassSchedule.objects.create(
#                                 course=routine.course,
#                                 teacher=routine.teacher,
#                                 room=routine.room,
#                                 date=current_date,
#                                 original_date=current_date,
#                                 semester=routine.batch,
#                                 start_time=routine.slot.start_time,
#                                 end_time=routine.slot.end_time,
#                                 status='pending',
#                                 class_type='offline',
#                             )
#                             created_count += 1
#                         except IntegrityError:
#                             skipped_conflicts += 1

#                 current_date += timedelta(days=1)

#             return created_count, deleted_count, skipped_conflicts
