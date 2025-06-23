from courses.models import Course

# List of courses with variable title and code, fixed semester and total_classes
courses_data = [
    {'title': 'Data Mining and Big Data Analysis ', 'code': 'CSE 451'},
    {'title': 'Data Mining and Big Data Analysis Lab', 'code': 'CSE 452'},
    {'title': 'Artificial Intelligence', 'code': 'CSE 453'},
    {'title': 'Artificial Intelligence Lab', 'code': 'CSE 454'},
    {'title': 'Software Quality Assurance', 'code': 'CSE 455'},
    {'title': 'Machine Learning ', 'code': 'CSE 457'},
    {'title': 'Machine Learning  Lab', 'code': 'CSE 458'},
    {'title': 'IoT Lab', 'code': 'CSE 460'},
    {'title': 'Research Project:', 'code': 'CSE 480'},
    

]

for data in courses_data:
    course = Course(
        title=data['title'],
        code=data['code'],
        semester='4-2',           # fixed semester
        total_classes=22          # fixed total classes
    )
    course.save()
    print(f"Saved course: {course.code} - {course.title} with ID {course.id}")


 #1_2  

#     {'title': 'Mathematics_2', 'code': 'MATH 151'},
#     {'title': 'Discrete Mathematics', 'code': 'CSE 153'},
#     {'title': 'Data Structure', 'code': 'CSE 155'},
#     {'title': 'Data Structure Lab', 'code': 'CSE 156'},
#     {'title': 'Electronics Devices & Circuit_1', 'code': 'CSE 157'},
#     {'title': 'Electronics Devices & Circuit_1 Lab', 'code': 'CSE 158'},
#     {'title': 'Object Oriented Programming (C++)', 'code': 'CSE 159'},
#     {'title': 'Object Oriented Programming (C++)', 'code': 'CSE 160'},
#     {'title': 'Technical Writing and Presentation Lab', 'code': 'CSE 162'},

# 2_1
#     {'title': 'Mathematics', 'code': 'MATH 201'},
#     {'title': 'Ethics and Cyber Law', 'code': 'CSE 203'},
#     {'title': 'Numerical Method', 'code': 'CSE 205'},
#     {'title': 'Numerical Method Lab', 'code': 'CSE 206'},
#     {'title': 'Electronics Devices & Circuit_2', 'code': 'CSE 207'},
#     {'title': 'Electronics Devices & Circuit_2 Lab', 'code': 'CSE 208'},
#     {'title': 'Algorithm_1', 'code': 'CSE 209'},
#     {'title': 'Algorithm_1 Lab', 'code': 'CSE 210'},
#     {'title': 'Object Oriented Programming (JAVA)', 'code': 'CSE 212'},