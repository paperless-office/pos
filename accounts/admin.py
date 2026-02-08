from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    Notice,
    Document,
    DepartmentDocument,
    ClassRoutine,
    Report,
    Assignment,
)

# ==========================
# Custom User Admin
# ==========================
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('id', 'email', 'username', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'user_type', 'profile_image')}),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'user_type',
                'password1',
                'password2',
                'is_staff',
                'is_active',
            ),
        }),
    )


# ==========================
# Notice Admin
# ==========================
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'notice_type', 'target', 'created_by', 'created_at')
    list_filter = ('notice_type', 'target')
    search_fields = ('title', 'description')


# ==========================
# Document Admin
# ==========================
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'target', 'created_at')
    list_filter = ('target',)
    search_fields = ('sender__email', 'receiver__email')


# ==========================
# Department Document Admin
# ==========================
@admin.register(DepartmentDocument)
class DepartmentDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_teacher', 'uploaded_by', 'created_at')
    list_filter = ('target_teacher',)
    search_fields = ('title',)


# ==========================
# Class Routine Admin
# ==========================
@admin.register(ClassRoutine)
class ClassRoutineAdmin(admin.ModelAdmin):
    list_display = ('semester', 'uploaded_at')
    ordering = ('semester',)


# ==========================
# Report Admin
# ==========================
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('sender', 'sender_type', 'is_responded', 'created_at')
    list_filter = ('sender_type', 'is_responded')
    search_fields = ('sender__username', 'message')


# ==========================
# Assignment Admin
# ==========================
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'assignment_name',
        'subject_name',
        'assignment_no',
        'student',
        'teacher',
        'submitted_at',
    )
    list_filter = ('teacher', 'subject_name')
    search_fields = ('assignment_name', 'student__email')
