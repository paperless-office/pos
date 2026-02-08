from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("redirect/", views.redirect_dashboard, name="redirect-dashboard"),
    path("department/", views.dept_dashboard, name="dept-dashboard"),
    path("teacher/", views.teacher_dashboard, name="teacher-dashboard"),
    path("student/", views.student_dashboard, name="student-dashboard"),
    path("create_notice/", views.create_notice, name="create_notice"),
    path("delete-notice/<int:id>/", views.delete_notice, name="delete_notice"),
    path("send-document/", views.send_document, name="send_document"),
    path("documents/upload/", views.upload_department_document, name="upload_document"),
    path("teacher/documents/", views.teacher_documents, name="teacher_documents"),
    path("teachers/", views.teachers_list, name="teachers_list"),
    path("teacher/documents/", views.teacher_documents, name="teacher_documents"),
    path("teachers/", views.teachers_list, name="teachers_list"),
    path("class-routine/", views.class_routine_view, name="class_routine"),
    path("report/send/", views.send_report, name="send_report"),
    path("reports/", views.view_reports, name="view_reports"),
    path("teacher/send-document/",views.teacher_send_document,name="teacher_send_document",),
    path("student/documents/", views.student_documents, name="student_documents"),
    path("teacher/notice/create/",views.teacher_notice_create,name="teacher_notice_create",),
    path("teacher/class-routine/",views.teacher_class_routine,name="teacher_class_routine",),
    path("student/submit-assignment/", views.submit_assignment, name="submit_assignment"),
    path("teacher/assignments/", views.teacher_assignments, name="teacher_assignments"),
    path("student/submit-assignment/", views.submit_assignment, name="submit_assignment"),
    path("student/class-routine/",views.student_class_routine,name="student_class_routine",),
    path("student/send-document/",views.student_send_document,name="student_send_document",),
    path('send-report/', views.send_report, name='send_report'),
    path('report/respond/<int:report_id>/', views.respond_report, name='respond_report'),
    # path('profile/update/', views.update_profile_image, name='update_profile_image'),
    path('profile/update/',views.update_profile_image,name='update_profile'),

    path(
    'student/notices/',
    views.student_all_notices,
    name='student_all_notices'
),

]
