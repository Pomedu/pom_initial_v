from django.forms import ModelForm, TextInput, ImageField, forms, FileInput

from studentapp.models import Student


class StudentCreationForm(ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'phone_number', 'phone_number_P', 'school',  'profile_photo']
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'placeholder': '학생이름을 입력하세요...'
            }),
            'phone_number': TextInput(attrs={
                'class': "form-control",
                'placeholder': '학생 휴대폰 번호를 입력하세요...'
            }),
            'phone_number_P': TextInput(attrs={
                'class': "form-control",
                'placeholder': '학부모 휴대폰 번호를 입력하세요...'
            }),
            'school': TextInput(attrs={
                'class': "form-control",
                'placeholder': '학생 학교명을 입력하세요...'
            }),
            'profile_photo': FileInput(attrs={
                'class': "form-control",
                'required': False,
            })

        }

        labels = {
            'name': '학생명',
            'phone_number': '학생 연락처',
            'phone_number_P': '학부모 연락처',
            'school': '학교명',
            'profile_photo': '사진'
        }
