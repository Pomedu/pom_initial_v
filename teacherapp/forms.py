from django import forms
from django.forms import ModelForm, TextInput, ImageField,FileInput, ModelChoiceField, BooleanField

from teacherapp.models import Teacher, Subject


class TeacherCreationForm(ModelForm):
    subject = ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(
        attrs={'class':'form-control'}),label='과목')

    class Meta:
        model = Teacher
        fields = ['name', 'phone_number', 'subject', 'profile_photo']
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'placeholder': '강사이름을 입력하세요...'
            }),
            'phone_number': TextInput(attrs={
                'class': "form-control",
                'placeholder': '강사 휴대폰 번호를 입력하세요...'
            }),
            'profile_photo': FileInput(attrs={
                'class': "form-control",
                'required': False,
            })

        }

        labels = {
            'name': '강사명',
            'phone_number': '강사 연락처',
            'profile_photo': '사진'
        }


class TeacherUpdateForm(ModelForm):
    subject = ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}), label='과목')
    is_active = BooleanField(label='활동 중')
    class Meta:
        model = Teacher
        fields = ['name', 'phone_number', 'subject', 'profile_photo', 'is_active']
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'placeholder': '강사이름을 입력하세요...'
            }),
            'phone_number': TextInput(attrs={
                'class': "form-control",
                'placeholder': '강사 휴대폰 번호를 입력하세요...'
            }),
            'profile_photo': FileInput(attrs={
                'class': "form-control",
                'required': False,
            }),


        }

        labels = {
            'name': '강사명',
            'phone_number': '강사 연락처',
            'profile_photo': '사진'
        }
