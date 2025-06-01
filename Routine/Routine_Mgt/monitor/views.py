from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from datetime import date
from routine.models import Routine
from monitor.models import ClassConductRecord

@staff_member_required
def admin_dashboard(request):
    today_date = date.today()  # date object, for filtering and weekday name
    today_str = today_date.strftime('%Y-%m-%d')  # string, to pass to template

    selected_batch = request.GET.get('batch', '3-2')

    weekday_name = today_date.strftime("%A")  # e.g. 'Monday'

    # Use weekday_name to filter routines for today
    todays_routines = Routine.objects.filter(batch=selected_batch, slot__day=weekday_name)

    routine_status_list = []
    for routine in todays_routines:
        record = ClassConductRecord.objects.filter(routine=routine, date=today_date).first()
        routine_status_list.append({
            'routine': routine,
            'status': record.status if record else 'pending'
        })

    return render(request, 'monitor/admin_dashboard.html', {
        'batches': ['1-2', '2-1', '3-1', '3-2', '4-2'],
        'selected_batch': selected_batch,
        'routine_status_list': routine_status_list,
        'today': today_str,  # pass string to template for input fields
    })

from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from django.http import JsonResponse
from .models import Routine, ClassConductRecord

@csrf_exempt
@staff_member_required
def mark_class_status(request):
    if request.method == 'POST':
        routine_id = request.POST.get('routine_id')
        date_str = request.POST.get('date')  # YYYY-MM-DD
        new_status = request.POST.get('status')

        try:
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

        try:
            routine = Routine.objects.get(id=routine_id)
        except Routine.DoesNotExist:
            return JsonResponse({'error': 'Routine not found'}, status=404)

        class_record, created = ClassConductRecord.objects.get_or_create(
            routine=routine,
            date=parsed_date,
            defaults={'status': new_status}
        )

        if not created:
            class_record.status = new_status
            class_record.save()

        return JsonResponse({
            'success': True,
            'routine_id': routine_id,
            'date': parsed_date.strftime('%Y-%m-%d'),
            'status': new_status,
            'created': created,
        })

    return JsonResponse({'error': 'Invalid request method'}, status=405)
