from django import forms
from django.forms import ModelForm, ModelChoiceField, ImageField, TextInput, Textarea, DateInput, NumberInput, \
    ChoiceField

from accountapp.models import User
from consultingapp.models import Consulting
from teacherapp.models import Teacher


class ConsultingCreationForm(ModelForm):
    status_choices = (
        ('P', '대기'),
        ('F', '완료'),
        ('N', '재상담요')
    )
    grade_choices = (
        ('M1', '중1'), ('M2', '중2'), ('M3', '중3'),
        ('H1', '고1'), ('H2', '고2'), ('H3', '고3'),
        ('E4', '초4'), ('E5', '초5'), ('E6', '초6')
    )
    in_charge_A = ModelChoiceField(queryset=User.objects.filter(role="A"), widget=forms.Select(
        attrs={'class': 'form-control'}), label='담당 직원')
    in_charge_T = ModelChoiceField(queryset=Teacher.objects.all(),widget=forms.Select(
        attrs={'class':'form-control'}),label='담당 강사')
    status = ChoiceField(choices= status_choices,widget=forms.Select(
        attrs={'class': 'form-control'}), label='상태')
    client_grade = ChoiceField(choices=grade_choices, widget=forms.Select(
        attrs={'class': 'form-control'}), label='학년')
    class Meta:
        model = Consulting
        fields = ['client_name', 'client_phone_number', 'client_school', 'client_grade',  'content', 'in_charge_A','in_charge_T', 'status']
        widgets = {
            'client_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': '상담 학생이름을 입력하세요...'
            }),
            'client_phone_number': TextInput(attrs={
                'class': "form-control",
                'placeholder': '고객 휴대폰 번호를 입력하세요...'
            }),
            'client_school': TextInput(attrs={
                'class': "form-control",
                'placeholder': '상담 학생 학교명을 입력하세요...'
            }),
            'content': Textarea(attrs={
                'class': "form-control",
                'rows': 5,
                'placeholder': '상담 내용을 입력하세요'
            })

        }

        labels = {
            'client_name': '고객명',
            'client_phone_number': '고객 번호',
            'client_school': '학교명',
            'content': '상담 내용',
        }
