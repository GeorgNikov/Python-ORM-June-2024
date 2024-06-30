import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student


def add_students():
    student = Student(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com'
    )
    student.save()

    student2 = Student()
    student2.student_id = 'FE0054'
    student2.first_name = 'Jane'
    student2.last_name = 'Smith'
    student2.email = 'jane.smith@university.com'
    student2.save()

    student3 = Student()
    student3.student_id = 'FH2014'
    student3.first_name = 'Alice'
    student3.last_name = 'Johnson'
    student3.birth_date = '1998-02-10'
    student3.email = 'alice.johnson@university.com'
    student3.save()

    student4 = Student()
    student4.student_id = 'FH2015'
    student4.first_name = 'Bob'
    student4.last_name = 'Wilson'
    student4.birth_date = '1996-11-25'
    student4.email = 'bob.wilson@university.com'
    student4.save()


def get_students_info():
    students = Student.objects.all()
    result = []
    for student in students:
        result.append(f"Student №{student.student_id}: "
                      f"{student.first_name} {student.last_name}; "
                      f"Email: {student.email}")

    return '\n'.join(result)


def update_students_emails():
    students = Student.objects.all()
    for student in students:
        student.email = student.email.replace(student.email.split('@')[1], 'uni-students.com')
        student.save()


def truncate_students():
    students = Student.objects.all()
    students.delete()

# Run and print your queries
