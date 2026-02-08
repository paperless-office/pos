from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Notice


# =========================
# SIGNUP FORM
# =========================
class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'user_type',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # REMOVE ALL DEFAULT DJANGO HELP TEXTS
        for field in self.fields.values():
            field.help_text = None


# LOGIN FORM
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # REMOVE HELP TEXTS (if any)
        for field in self.fields.values():
            field.help_text = None


# =========================
# NOTICE FORM
# =========================
class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description', 'target']



from .models import Document

class DocumentForm(forms.ModelForm):
    SEND_CHOICES = (
        ('all', 'All Teachers'),
        ('single', 'Single Teacher'),
    )

    send_type = forms.ChoiceField(
        choices=SEND_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Document
        fields = ['file']




from django import forms
from .models import DepartmentDocument

class DepartmentDocumentForm(forms.ModelForm):
    class Meta:
        model = DepartmentDocument
        fields = ['title', 'file', 'target_teacher']


from .models import ClassRoutine

class ClassRoutineForm(forms.ModelForm):
    class Meta:
        model = ClassRoutine
        fields = ['file']




from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Write your report here...'
            })
        }



class TeacherSendDocumentForm(forms.ModelForm):
    TARGET_CHOICES = (
        ('department', 'Send to Department'),
        ('all_students', 'Send to All Students'),
        ('single_student', 'Send to Single Student'),
    )

    target = forms.ChoiceField(
        choices=TARGET_CHOICES,
        widget=forms.RadioSelect
    )

    student = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(user_type='student'),
        required=False
    )

    class Meta:
        model = Document
        fields = ['file']


class TeacherNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description']






from .models import Assignment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            'subject_name',
            'assignment_name',
            'assignment_no',
            'teacher',
            'file'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # dropdown এ শুধু teacher দেখাবে
        self.fields['teacher'].queryset = CustomUser.objects.filter(
            user_type='teacher'
        )

        for field in self.fields.values():
            field.help_text = None


class StudentSendDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['receiver', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # dropdown এ শুধু teachers
        self.fields['receiver'].queryset = CustomUser.objects.filter(
            user_type='teacher'
        )

        self.fields['receiver'].label = "Select Teacher"


from .models import Assignment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            'subject_name',
            'assignment_name',
            'assignment_no',
            'teacher',
            'file'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # dropdown এ শুধু teacher দেখাবে
        self.fields['teacher'].queryset = CustomUser.objects.filter(
            user_type='teacher'
        )

        for field in self.fields.values():
            field.help_text = None


from django import forms
from .models import Document, CustomUser

class StudentSendDocumentForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(user_type='teacher'),
        label='Select Teacher'
    )

    class Meta:
        model = Document
        fields = ['file']


from django import forms
from .models import CustomUser

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image']
