from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Course
from teachers.models import ClassSchedule
from django.utils.html import format_html
from django.db.models import Count, Q

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'semester', 'class_statistics')
    list_filter = ('title','semester', 'code')
    def class_statistics(self, obj):
        stats = ClassSchedule.objects.filter(course=obj)

        total = stats.count()
        conducted = stats.filter(status='conducted').count()
        cancelled = stats.filter(status='cancelled').count()
        rescheduled = stats.filter(status='rescheduled').count()
        pending = stats.filter(status='pending').count()
        missed =  stats.filter(status='missed').count()
        

        # offline = stats.filter(class_type='offline').count()
        # online = stats.filter(class_type='online').count()

        return format_html(
            "<ul style='padding-left:16px;'>"
            "<li><strong>Total:</strong> {}</li>"
            "<li>✅ Conducted: {}</li>"
            "<li>♻️ Rescheduled: {}</li>"
            "<li>❌ Cancelled: {}</li>"
            "<li>⏳ Pending: {}</li>"
            "<li>🚫 Missed: {}</li>" 
            # "<li>💻 Online: {}</li>"
            # "<li>🏫 Offline: {}</li>"
            "</ul>",
            total, conducted, rescheduled, cancelled, pending,missed,# online, offline
        )

    class_statistics.short_description = "📊 Class Stats"
    class_statistics.allow_tags = True

admin.site.register(Course, CourseAdmin)
