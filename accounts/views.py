# from django.shortcuts import render
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Notice
# from .forms import NoticeForm

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login
# from django.contrib.auth.views import LoginView
# from django.db import models
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import DepartmentDocument
# from .forms import DepartmentDocumentForm

from .forms import TeacherSendDocumentForm
from .forms import TeacherNoticeForm
from .models import Assignment
from .forms import AssignmentForm
from .forms import StudentSendDocumentForm
from .forms import ProfileImageForm








from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.db import models
from .models import Document
from .models import Report
from .forms import ReportForm


from .models import Notice, DepartmentDocument
from .forms import NoticeForm, DepartmentDocumentForm

from .models import CustomUser, Notice, Document

# ===== IMPORT FORMS =====
from .forms import (
    SignupForm,
    LoginForm,
    NoticeForm,
    DocumentForm
)


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('redirect-dashboard')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login.html'


@login_required
def redirect_dashboard(request):
    if request.user.user_type == 'department_head':
        return redirect('dept-dashboard')
    elif request.user.user_type == 'teacher':
        return redirect('teacher-dashboard')
    else:
        return redirect('student-dashboard')





from .models import Notice
from .forms import NoticeForm

# @login_required
# def dept_dashboard(request):
#     if request.user.user_type != 'department_head':
#         return redirect('login')

#     notices = Notice.objects.filter(created_by=request.user)

  

#     return render(request, 'accounts/dept_dashboard.html', {
        
#         'notices': notices
#     })

@login_required
def dept_dashboard(request):
    if request.user.user_type != 'department_head':
        return redirect('login')

    notices = Notice.objects.filter(
        target__in=['both', 'teacher', 'student']
    ).order_by('-created_at')

    return render(request, 'accounts/dept_dashboard.html', {
        'notices': notices
    })





from django.db.models import Q

@login_required
def teacher_dashboard(request):
    if request.user.user_type != 'teacher':
        return redirect('login')

    notices = Notice.objects.filter(
        Q(created_by=request.user, notice_type='teacher') |
        Q(notice_type='department', target='teacher') |
        Q(notice_type='department', target='both')
    ).order_by('-created_at')[:2]   # 🔥 FIRST 2 ONLY

    return render(request, 'accounts/teacher_dashboard.html', {
        'notices': notices
    })



# @login_required
# def student_dashboard(request):
#     if request.user.user_type != 'student':
#         return redirect('login')

#     notices = Notice.objects.filter(
#         target__in=['student', 'both'],
#         notice_type='department'
#     ).order_by('-created_at')

#     teacher_notices = Notice.objects.filter(
#         target='student',
#         notice_type='teacher'
#     ).select_related('created_by').order_by('-created_at')

#     return render(request, 'accounts/student_dashboard.html', {
#         'notices': notices,
#         'teacher_notices': teacher_notices,
#     })

from django.db.models import Q

@login_required
def student_dashboard(request):
    if request.user.user_type != 'student':
        return redirect('login')

    notices = Notice.objects.filter(
        Q(notice_type='department', target__in=['student', 'both']) |
        Q(notice_type='teacher', target='student')
    ).order_by('-created_at')

    return render(request, 'accounts/student_dashboard.html', {
        'notices': notices,   # 👈 full list পাঠানো হচ্ছে
    })





# Notice Management

@login_required
def create_notice(request):

    if request.user.user_type != 'department_head':
        return redirect('login')

    notices = Notice.objects.filter(created_by=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user
            notice.save()
            return redirect('create_notice')
    else:
        form = NoticeForm()

    return render(request, 'accounts/create_notice.html', {
        'form': form,
        'notices': notices
    })


# Delete Notice
@login_required
def delete_notice(request, id):
    notice = get_object_or_404(Notice, id=id, created_by=request.user)
    notice.delete()
    return redirect('create_notice')






# @login_required
# def send_document(request):
#     if request.user.user_type != 'department_head':
#         return redirect('login')

#     teachers = CustomUser.objects.filter(user_type='teacher')

#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         send_type = request.POST.get('send_type')
#         teacher_id = request.POST.get('teacher')

#         if form.is_valid():
#             if send_type == 'all':
#                 Document.objects.create(
#                     sender=request.user,
#                     send_to_all=True,
#                     file=request.FILES['file']
#                 )
#             else:
#                 teacher = CustomUser.objects.get(id=teacher_id)
#                 Document.objects.create(
#                     sender=request.user,
#                     receiver=teacher,
#                     send_to_all=False,
#                     file=request.FILES['file']
#                 )

#             return redirect('dept-dashboard')
#     else:
#         form = DocumentForm()

#     return render(request, 'accounts/send_document.html', {
#         'form': form,
#         'teachers': teachers
#     })


@login_required
def send_document(request):
    if request.user.user_type != 'department_head':
        return redirect('login')

    # ====== SECTION 1: Send document (existing feature) ======
    teachers = CustomUser.objects.filter(user_type='teacher')

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        send_type = request.POST.get('send_type')
        teacher_id = request.POST.get('teacher')

        if form.is_valid():
            if send_type == 'all':
                Document.objects.create(
                    sender=request.user,
                    target='all_teachers',
                    file=request.FILES['file']
                )
            else:
                teacher = get_object_or_404(CustomUser, id=teacher_id)
                Document.objects.create(
                    sender=request.user,
                    receiver=teacher,
                    target='single_teacher',
                    file=request.FILES['file']
                )

            return redirect('send_document')
    else:
        form = DocumentForm()

    # ====== SECTION 2: Documents sent TO department ======
    incoming_documents = Document.objects.filter(
        target='department'
    ).order_by('-created_at')

    return render(request, 'accounts/send_document.html', {
        'form': form,
        'teachers': teachers,
        'incoming_documents': incoming_documents,
    })





# document view to teacher pannel
@login_required
def upload_department_document(request):
    if request.user.user_type != 'department_head':
        return redirect('login')

    if request.method == 'POST':
        form = DepartmentDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user

            if not doc.target_teacher:
                doc.target_teacher = None  

            doc.save()
            return redirect('dept-dashboard')
    else:
        form = DepartmentDocumentForm()

    return render(request, 'accounts/upload_document.html', {
        'form': form
    })



@login_required
def teacher_documents(request):
    if request.user.user_type != 'teacher':
        return redirect('login')

    documents = Document.objects.filter(
        models.Q(target='department') |
        models.Q(receiver=request.user)
    ).order_by('-created_at')

    return render(request, 'accounts/teacher_documents.html', {
        'documents': documents
    })




# View teachers list at department pannel

@login_required
def teachers_list(request):
    if request.user.user_type != 'department_head':
        return redirect('login')

    teachers = CustomUser.objects.filter(user_type='teacher')

    return render(request, 'accounts/teachers_list.html', {
        'teachers': teachers
    })



# routine
import os
from .models import ClassRoutine
from .forms import ClassRoutineForm

@login_required
def class_routine_view(request):
    if request.user.user_type != 'department_head':
        return redirect('login')

    routines = {}
    for i in range(1, 9):
        routines[i] = ClassRoutine.objects.filter(semester=i).first()

    if request.method == 'POST':
        semester = int(request.POST.get('semester'))
        form = ClassRoutineForm(request.POST, request.FILES)

        if form.is_valid():
            routine, created = ClassRoutine.objects.get_or_create(
                semester=semester
            )

            # delete old file if exists
            if routine.file:
                if os.path.isfile(routine.file.path):
                    os.remove(routine.file.path)

            routine.file = request.FILES['file']
            routine.save()

            return redirect('class_routine')

    return render(request, 'accounts/class_routine_department.html', {
        'routines': routines
    })




# teachers / student send reports

@login_required
def send_report(request):
    if request.user.user_type not in ['teacher', 'student']:
        return redirect('login')

    reports = Report.objects.filter(sender=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.sender = request.user
            report.sender_type = request.user.user_type
            report.save()
            return redirect('send_report')
    else:
        form = ReportForm()

    return render(request, 'accounts/send_report.html', {
        'form': form,
        'reports': reports
    })



# Department view reports

@login_required
def view_reports(request):
    if request.user.user_type != 'department_head':
        return redirect('login')

    reports = Report.objects.all().order_by('-created_at')

    return render(request, 'accounts/view_reports.html', {
        'reports': reports
    })



#Teacher Documents Page Update

@login_required
def teacher_send_document(request):
    if request.user.user_type != 'teacher':
        return redirect('login')

    students = CustomUser.objects.filter(user_type='student')

    if request.method == 'POST':
        form = TeacherSendDocumentForm(request.POST, request.FILES)
        target = request.POST.get('target')
        student_id = request.POST.get('student')

        if form.is_valid():
            if target == 'department':
                Document.objects.create(
                    sender=request.user,
                    target='department',
                    file=request.FILES['file']
                )

            elif target == 'all_students':
                Document.objects.create(
                    sender=request.user,
                    target='all_students',
                    file=request.FILES['file']
                )

            else:
                student = get_object_or_404(CustomUser, id=student_id)
                Document.objects.create(
                    sender=request.user,
                    receiver=student,
                    target='single_student',
                    file=request.FILES['file']
                )

            return redirect('teacher_documents')
    else:
        form = TeacherSendDocumentForm()

    return render(request, 'accounts/teacher_send_document.html', {
        'form': form,
        'students': students
    })



# Student document view
@login_required
def student_documents(request):
    if request.user.user_type != 'student':
        return redirect('login')

    documents = Document.objects.filter(
        models.Q(target='all_students') |
        models.Q(receiver=request.user)
    ).order_by('-created_at')

    return render(request, 'accounts/student_documents.html', {
        'documents': documents
    })





#Teacher Notice Create
# @login_required
# def teacher_notice_create(request):
#     if request.user.user_type != 'teacher':
#         return redirect('login')

#     notices = Notice.objects.filter(
#         created_by=request.user,
#         notice_type='teacher'
#     ).order_by('-created_at')

#     if request.method == 'POST':
#         form = TeacherNoticeForm(request.POST)
#         if form.is_valid():
#             notice = form.save(commit=False)
#             notice.created_by = request.user
#             notice.target = 'student'
#             notice.notice_type = 'teacher'
#             notice.save()
#             return redirect('teacher_notice_create')
#     else:
#         form = TeacherNoticeForm()

#     return render(request, 'accounts/teacher_notice_create.html', {
#         'form': form,
#         'notices': notices
#     })


from django.db.models import Q

@login_required
def teacher_notice_create(request):
    if request.user.user_type != 'teacher':
        return redirect('login')

    # 🔥 ALL NOTICES FOR TEACHER PANEL
    notices = Notice.objects.filter(
        Q(created_by=request.user, notice_type='teacher') |
        Q(notice_type='department', target='teacher') |
        Q(notice_type='department', target='both')
    ).order_by('-created_at')

    if request.method == 'POST':
        form = TeacherNoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user
            notice.notice_type = 'teacher'
            notice.target = 'student'   # teacher → students
            notice.save()
            return redirect('teacher_notice_create')
    else:
        form = TeacherNoticeForm()

    return render(request, 'accounts/teacher_notice_create.html', {
        'form': form,
        'notices': notices
    })




#teachers routine view

@login_required
def teacher_class_routine(request):
    if request.user.user_type != 'teacher':
        return redirect('login')

    semester = request.GET.get('semester')

    if semester:
        routines = ClassRoutine.objects.filter(semester=semester)
    else:
        routines = ClassRoutine.objects.all().order_by('semester')

    return render(request, 'accounts/teacher_class_routine.html', {
        'routines': routines,
        'selected_semester': semester,
        'semesters': range(1, 9),
    })






#Assaignment Sb
@login_required
def submit_assignment(request):
    if request.user.user_type != 'student':
        return redirect('login')

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.save()
            return redirect('student-dashboard')
    else:
        form = AssignmentForm()

    return render(request, 'accounts/submit_assignment.html', {
        'form': form
    })


#Teachers dashboard view assaignment
@login_required
def teacher_assignments(request):
    if request.user.user_type != 'teacher':
        return redirect('login')

    assignments = Assignment.objects.filter(
        teacher=request.user
    ).order_by('-submitted_at')

    return render(request, 'accounts/teacher_assignments.html', {
        'assignments': assignments
    })



#submit assaignment view
@login_required
def submit_assignment(request):
    if request.user.user_type != 'student':
        return redirect('login')

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.save()
            return redirect('student-dashboard')
    else:
        form = AssignmentForm()

    return render(request, 'accounts/submit_assignment.html', {
        'form': form
    })




#student routine view
@login_required
def student_class_routine(request):
    if request.user.user_type != 'student':
        return redirect('login')

    semester = request.GET.get('semester')

    if semester:
        routines = ClassRoutine.objects.filter(semester=semester)
    else:
        routines = ClassRoutine.objects.all().order_by('semester')

    return render(request, 'accounts/student_class_routine.html', {
        'routines': routines,
        'selected_semester': semester,
        'semesters': range(1, 9),
    })




#send document student to teacher

@login_required
def student_send_document(request):
    if request.user.user_type != 'student':
        return redirect('login')

    if request.method == 'POST':
        form = StudentSendDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.cleaned_data['teacher']

            Document.objects.create(
                sender=request.user,
                receiver=teacher,
                target='single_student',
                file=form.cleaned_data['file']
            )

            return redirect('student_documents')
    else:
        form = StudentSendDocumentForm()

    return render(request, 'accounts/student_send_document.html', {
        'form': form
    })




# Response feedback
@login_required
def respond_report(request, report_id):
    if request.user.user_type != 'department_head':
        return redirect('login')

    report = get_object_or_404(Report, id=report_id)

    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        report.feedback = feedback
        report.is_responded = True
        report.save()
        return redirect('view_reports')

    return redirect('view_reports')



#update profile
@login_required
def update_profile_image(request):
    if request.method == 'POST':
        form = ProfileImageForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('redirect-dashboard')
    else:
        form = ProfileImageForm(instance=request.user)

    return render(request, 'accounts/update_profile_image.html', {
        'form': form
    })





#student all notice

from django.db.models import Q

@login_required
def student_all_notices(request):
    if request.user.user_type != 'student':
        return redirect('login')

    notices = Notice.objects.filter(
        Q(notice_type='department', target__in=['student', 'both']) |
        Q(notice_type='teacher', target='student')
    ).order_by('-created_at')

    return render(request, 'accounts/student_all_notices.html', {
        'notices': notices
    })
