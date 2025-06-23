# from django.contrib import admin

# # Register your models here.
# from django.contrib import admin
# from django.utils.html import format_html
# from django.urls import path
# from django.shortcuts import get_object_or_404, redirect
# from django.contrib import messages
# from django.db.models import Count
# from .models import DailyClassLog
# from datetime import datetime

# @admin.register(DailyClassLog)
# class DailyClassLogAdmin(admin.ModelAdmin):
#     list_display = ('course', 'teacher', 'semester', 'date', 'start_time', 'end_time', 'status', 'mark_button')
#     list_filter = ('semester', 'status', 'date', 'course')
#     search_fields = ('course__code', 'teacher__name')
#     actions = ['view_course_stats', 'auto_mark_missed']

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('<int:pk>/mark_conducted/', self.admin_site.admin_view(self.mark_conducted), name='mark_conducted'),
#         ]
#         return custom_urls + urls

#     def mark_button(self, obj):
#         if obj.status == 'pending':
#             return format_html(
#                 '<a class="button" href="{}">✅ Mark Conducted</a>',
#                 f"{obj.pk}/mark_conducted/"
#             )
#         return obj.status.capitalize()
#     mark_button.short_description = "Status"

#     def mark_conducted(self, request, pk):
#         log = get_object_or_404(DailyClassLog, pk=pk)
#         if log.status == 'pending':
#             log.status = 'conducted'
#             log.save()
#             self.message_user(request, f"{log.course.code} on {log.date} marked as conducted.")
#         return redirect(request.META.get('HTTP_REFERER'))

#     def view_course_stats(self, request, queryset):
#         if queryset.count() != 1:
#             self.message_user(request, "Select exactly one course log to view stats.", level=messages.WARNING)
#             return
#         course = queryset.first().course
#         stats = DailyClassLog.objects.filter(course=course).values('status').annotate(total=Count('id'))
#         msg = f"Stats for {course.code}: " + ", ".join(f"{s['status']}={s['total']}" for s in stats)
#         self.message_user(request, msg)
#     view_course_stats.short_description = "📊 View Stats for selected course"

#     def auto_mark_missed(self, request, queryset):
#         now = datetime.now()
#         count = 0
#         for log in queryset.filter(status='pending'):
#             class_end = datetime.combine(log.date, log.end_time)
#             if now > class_end:
#                 log.status = 'missed'
#                 log.save()
#                 count += 1
#         self.message_user(request, f"{count} pending classes auto-marked as missed.")
#     auto_mark_missed.short_description = "⏱ Auto-mark missed classes"
