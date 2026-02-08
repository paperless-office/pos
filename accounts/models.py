from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('department_head', 'Department Head'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    # ✅ PROFILE IMAGE
    profile_image = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.png',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username



class Notice(models.Model):
    NOTICE_TARGET_CHOICES = (
        ('teacher', 'Teachers'),
        ('student', 'Students'),
        ('both', 'Teachers & Students'),
    )

    NOTICE_TYPE_CHOICES = (
        ('department', 'Department'),
        ('teacher', 'Teacher'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    target = models.CharField(max_length=10, choices=NOTICE_TARGET_CHOICES)

    notice_type = models.CharField(
        max_length=20,
        choices=NOTICE_TYPE_CHOICES,
        default='department'
    )

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



#document file 

from .models import CustomUser 

class Document(models.Model):
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_documents'
    )

    receiver = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='received_documents'
    )

    send_to_all = models.BooleanField(default=False)

    file = models.FileField(upload_to='documents/')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.send_to_all:
            return f"Document to all teachers"
        return f"Document to {self.receiver.email}"



# Document resived to teachers
class DepartmentDocument(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='department_documents/')
    
    # null = all teachers
    target_teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'user_type': 'teacher'}
    )

    uploaded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='uploaded_documents',
        limit_choices_to={'user_type': 'department_head'}
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# routine

class ClassRoutine(models.Model):
    SEMESTER_CHOICES = [
        (1, '1st Semester'),
        (2, '2nd Semester'),
        (3, '3rd Semester'),
        (4, '4th Semester'),
        (5, '5th Semester'),
        (6, '6th Semester'),
        (7, '7th Semester'),
        (8, '8th Semester'),
    ]

    semester = models.PositiveSmallIntegerField(
        choices=SEMESTER_CHOICES,
        unique=True
    )

    file = models.FileField(upload_to='class_routines/')

    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Semester {self.semester} Routine"





# report 

class Report(models.Model):
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reports'
    )

    sender_type = models.CharField(max_length=20)  # teacher / student

    message = models.TextField()

    # ✅ NEW FIELDS
    feedback = models.TextField(blank=True, null=True)
    is_responded = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} report"






#document
class Document(models.Model):
    TARGET_CHOICES = (
        ('department', 'Department'),
        ('all_students', 'All Students'),
        ('single_student', 'Single Student'),
    )

    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_documents'
    )

    receiver = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='received_documents'
    )

    target = models.CharField(
        max_length=20,
        choices=TARGET_CHOICES
    )

    file = models.FileField(upload_to='documents/')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.email} → {self.target}"




#Assaignment

class Assignment(models.Model):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='submitted_assignments',
        limit_choices_to={'user_type': 'student'}
    )

    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_assignments',
        limit_choices_to={'user_type': 'teacher'}
    )

    subject_name = models.CharField(max_length=100)
    assignment_name = models.CharField(max_length=150)
    assignment_no = models.CharField(max_length=50)

    file = models.FileField(upload_to='assignments/')

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assignment_name} - {self.student.email}"
