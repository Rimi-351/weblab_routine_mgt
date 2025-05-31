from django.contrib.auth.models import User
from teachers.models import Teacher

password = "123456"
designation = "Lecturer"
department = "CSE"

teacher_names = [

#     "Abul Kalam Azad",
#     "Abu Sayed Md.Mustafizur Rahanman",
#     "Jugal Krishna Das",
#     "Ezharul Islam",
#     "Liton Jude Rozario",
#     "Morium Akter",
#     "Imdadul Islam",
#     "Md. Shorif Uddin",
#     "Md. Zahidur Rahman",
#     "Md. Golam Moazzam",
#     "Israt Jahan",
#     "Md. Humayun Kabir",
#     "Sanjit Kumar Saha",
#     "Md. Musfique Anwar",
#     "Sarnali Basak",
#     "Amina Khatun",
#     "Tahsina Hashem",
#     "Tanzila Rahman",
#     "Md Rafsan Jani",
#     "Hafsa Moontari",
#     "Sabrina Sharmin",
#     "Md Asraful Islam",
#     "Bulbul Ahammad",
#     "Anup Podder",
#      "Nadia Afrin Ritu",
#      "Sansun Nahar Khandakar",       
#      "Md Masum Bhuiyan",
  
]

def acronym(name):
    return ''.join(word[0].lower() for word in name.split())

for full_name in teacher_names:
    username = acronym(full_name)
    email = f"{username}@juniv.edu"
    user = User.objects.create_user(username=username, password=password, email=email, first_name=full_name.split()[0], last_name=' '.join(full_name.split()[1:]))
    teacher = Teacher.objects.create(
        user=user,
        name=full_name,
        email=email,
        designation=designation,
        department=department
    )
    print(f"Created teacher: {full_name} with username: {username}")

