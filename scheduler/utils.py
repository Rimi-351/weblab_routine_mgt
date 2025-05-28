# from datetime import date
# from .models import AcademicWeek

# def get_current_academic_week():
#     today = date.today()
#     return AcademicWeek.objects.filter(start_date__lte=today, end_date__gte=today).first()

# def is_class_week():
#     current = get_current_academic_week()
#     if not current:
#         return False
#     return "Week" in current.label and "Exam" not in current.label and "Prep" not in current.label

# # utils.py
# from datetime import datetime

# def get_current_academic_week():
#     # Example logic to determine current academic week
#     current_date = datetime.today()
#     # Replace with your actual logic to find academic week based on your calendar
#     if current_date.month in [1, 2, 3]:  # Example: classes start in January
#         return {"label": "Week 5", "start_date": "2025-05-01"}
#     elif current_date.month in [4, 5, 6]:
#         return {"label": "Exam Week", "start_date": "2025-05-01"}
#     else:
#         return None

# # utils.py
# from .models import AcademicWeek

# def is_class_week():
#     # Get the current date
#     today = datetime.today().date()

#     # Retrieve the current academic week (modify the query as per your logic)
#     current_week = AcademicWeek.objects.filter(start_date__lte=today, end_date__gte=today).first()

#     # Ensure current_week is an instance of AcademicWeek
#     if current_week:
#         return current_week
#     return None  # No class week found

from datetime import datetime
from .models import AcademicWeek

def get_current_academic_week():
    """
    This function returns the current active academic week if there is one, 
    or None if there isn't.
    """
    today = datetime.today().date()

    # Find the academic week that includes the current date
    current_week = AcademicWeek.objects.filter(start_date__lte=today, end_date__gte=today).first()

    # Return the AcademicWeek instance (if found)
    return current_week

def is_class_week():
    """
    This function checks if the current date falls within an active academic week.
    Returns True if there is an active class week, otherwise False.
    """
    current_week = get_current_academic_week()

    # Check if there is a valid academic week
    return current_week is not None
