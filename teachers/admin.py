from django.contrib import admin
from django import forms
from django.db import IntegrityError
from .models import Teacher, Reschedule, ClassSchedule
from .forms import RescheduleForm
from django.utils.safestring import mark_safe
from routine.models import Routine
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.timezone import now
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ScheduleGenerationForm
from routine.models import Routine, Vacation
from .models import ClassSchedule
from datetime import timedelta


@admin.register(Reschedule)
class RescheduleAdmin(admin.ModelAdmin):
    form = RescheduleForm
    list_display = ['class_schedule', 'reschedule_date', 'is_online', 'new_start_time', 'new_end_time']

    fieldsets = (
        (None, {
            'fields': ('class_schedule', 'reschedule_date', 'is_online')
        }),
        ('Online Class Details', {
            'fields': ('online_duration',),
            'classes': ('collapse',)
        }),
        ('Offline Class Details', {
            'fields': ('offline_duration', 'room',),
            'classes': ('collapse',)
        }),
        ('Timing', {
            'fields': ('new_start_time', 'new_end_time'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Offline slot help text
        form.base_fields['room'].help_text = mark_safe(
            '<a href="http://127.0.0.1:8000/routine/available-slots/" target="_blank" style="color: green;">Check Offline Available Slots</a>'
        )

        # ✅ Online slot help text
        form.base_fields['online_duration'].help_text = mark_safe(
            '<a href="http://127.0.0.1:8000/teachers/online-reschedules/" target="_blank" style="color: blue;">Check Online Available Slots</a>'
        )

        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # After saving Reschedule, update the related ClassSchedule
        class_schedule = obj.class_schedule
        class_schedule.date = obj.reschedule_date
        if obj.new_start_time:
            class_schedule.start_time = obj.new_start_time
        if obj.new_end_time:
            class_schedule.end_time = obj.new_end_time
        class_schedule.save()

        # Update Routine if exists
        try:
            routine = Routine.objects.get(
                teacher=class_schedule.teacher,
                course__title=class_schedule.subject,
            )
            routine.status = 'rescheduled'
            routine.is_cancelled = False
            routine.slot.start_time = obj.new_start_time or routine.slot.start_time
            routine.slot.end_time = obj.new_end_time or routine.slot.end_time
            routine.save()

            Notification.objects.create(
                title="Class Rescheduled",
                message=f"{routine.course.title} class has been rescheduled to {obj.new_start_time} - {obj.new_end_time}.",
            )
        except Routine.DoesNotExist:
            pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'designation', 'department']
    search_fields = ['name', 'email', 'department']

from django.contrib import admin
from teachers.models import ClassSchedule
from datetime import datetime

class SpecificDateFilter(admin.SimpleListFilter):
    title = 'Date (Exact)'
    parameter_name = 'date_exact'

    def lookups(self, request, model_admin):
        return []

    def queryset(self, request, queryset):
        value = request.GET.get(self.parameter_name)
        if value:
            try:
                date_value = datetime.strptime(value, '%Y-%m-%d').date()
                return queryset.filter(date=date_value)
            except ValueError:
                return queryset.none()
        return queryset

def generate_class_schedule(start_date, end_date):
    day_name_to_num = {
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2,
        'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6,
    }
    routines = Routine.objects.all()
    vacation_dates = set()
    for v in Vacation.objects.all():
        current = v.start_date
        while current <= v.end_date:
            vacation_dates.add(current)
            current += timedelta(days=1)


    deleted_count, _ = ClassSchedule.objects.filter(date__range=(start_date, end_date)).delete()

    created_count = 0
    skipped_conflicts = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date in vacation_dates:
            current_date += timedelta(days=1)
            continue

        weekday_num = current_date.weekday()

        for routine in routines:
            if day_name_to_num.get(routine.slot.day) == weekday_num:
                if ClassSchedule.objects.filter(
                    room=routine.room,
                    date=current_date,
                    start_time=routine.slot.start_time
                ).exists():
                    skipped_conflicts += 1
                    continue

                try:
                    ClassSchedule.objects.create(
                        course=routine.course,
                        teacher=routine.teacher,
                        room=routine.room,
                        date=current_date,
                        original_date=current_date,
                        semester=routine.batch,
                        start_time=routine.slot.start_time,
                        end_time=routine.slot.end_time,
                        status='pending',
                        class_type='offline',
                    )
                    created_count += 1
                except IntegrityError:
                    skipped_conflicts += 1

        current_date += timedelta(days=1)

    return created_count, deleted_count, skipped_conflicts

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'date', 'semester', 'start_time', 'end_time', 'room', 'status', 'class_type', 'mark_button')
    list_filter = (
        SpecificDateFilter,   # 👈 add this custom filter
        'semester',
        'course',
        'status', 'class_type', 'teacher',
    )
    actions = ['mark_as_missed','mark_as_conducted','auto_mark_missed', 'generate_schedules']
    search_fields = ('date','course__title', 'teacher__name')

    def generate_schedule_view(self, request):
        if request.method == 'POST':
            form = ScheduleGenerationForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                created, deleted, conflicts = generate_class_schedule(start_date, end_date)
                self.message_user(request, f"✅ {created} created, 🗑️ {deleted} deleted, ❌ {conflicts} conflicts.")
                return redirect('..')
        else:
            form = ScheduleGenerationForm()

        return render(request, 'admin/generate_class_schedule.html', {'form': form})

    @admin.action(description="✅ Mark selected classes as Conducted")
    def mark_as_conducted(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='conducted')
        self.message_user(request, f"{updated} class(es) marked as conducted.")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/mark_conducted/', self.admin_site.admin_view(self.mark_conducted), name='schedule_mark_conducted'),
             path('generate-schedules/', self.admin_site.admin_view(self.generate_schedule_view), name='generate_schedules')
        ]
        return custom_urls + urls

    def mark_button(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="{}">✅ Mark Conducted</a>',
                f"{obj.pk}/mark_conducted/"
            )
        return obj.status.capitalize()
    mark_button.short_description = "Status"

    def mark_conducted(self, request, pk):
        schedule = get_object_or_404(ClassSchedule, pk=pk)
        if schedule.status == 'pending':
            schedule.status = 'conducted'
            schedule.save()
            self.message_user(request, f"{schedule.course.code} on {schedule.date} marked as conducted.")
        return redirect(request.META.get('HTTP_REFERER'))

    def auto_mark_missed(self, request, queryset):
        current_time = now()
        count = 0
        for cs in queryset.filter(status='pending'):
            class_end = datetime.combine(cs.date, cs.end_time)
            if current_time > class_end:
                cs.status = 'missed'
                cs.save()
                count += 1
        self.message_user(request, f"{count} pending classes auto-marked as missed.")
    auto_mark_missed.short_description = "⏱ Auto-mark missed classes"

    @admin.action(description="❌ Mark selected classes as missed")
    def mark_as_missed(self, request, queryset):
        missed = 0
        for schedule in queryset.filter(status='pending'):
            schedule.status = 'missed'
            schedule.save()
            missed += 1
        self.message_user(request, f"{missed} class(es) marked as missed.", level=messages.WARNING)

