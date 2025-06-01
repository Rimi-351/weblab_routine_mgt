# from django.contrib import admin
# from .models import Teacher, Batch, Course, Room, ScheduleEntry
# from .utils import is_class_week, get_current_academic_week
# from django.http import HttpResponseForbidden

# class ScheduleEntryAdmin(admin.ModelAdmin):
#     # Restrict add permission based on the current academic week
#     def has_add_permission(self, request):
#         # Check if the current week is an academic week
#         if not is_class_week():
#             return False
#         return True

#     # Display the current academic week in the admin list view
#     def changelist_view(self, request, extra_context=None):
#         # Get the current academic week and pass it to the admin context
#         extra_context = extra_context or {}
#         current_week = get_current_academic_week()

#         if current_week:  # Only add the current week if it's found
#             extra_context['current_week'] = current_week.label

#         return super().changelist_view(request, extra_context=extra_context)

# admin.site.register([Teacher, Batch, Course, Room])
# admin.site.register(ScheduleEntry, ScheduleEntryAdmin)

from django.contrib import admin
from .models import Teacher, Batch, Course, Room, ScheduleEntry
from .utils import is_class_week, get_current_academic_week
from django.http import HttpResponseForbidden

class ScheduleEntryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Restrict adding new schedule entries if it's not an academic week
        if not is_class_week():
            return False
        return True

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        current_week = get_current_academic_week()

        if current_week:  # Only add current_week to context if found
            extra_context['current_week'] = current_week.label

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register([Teacher, Batch, Course, Room])
admin.site.register(ScheduleEntry, ScheduleEntryAdmin)
