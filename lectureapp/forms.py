from django import forms
from django.forms import ModelForm, ModelChoiceField, ImageField, TextInput, Textarea, DateInput, NumberInput, \
    ChoiceField, TimeInput

from lectureapp.models import Lecture, CourseTime, CourseRegistration
from studentapp.models import Student
from teacherapp.models import Teacher


class LectureCreationForm(ModelForm):
    status_choices = (
        ('P', '대기'),
        ('O', '진행중'),
        ('F', '종강'),
    )
    teacher = ModelChoiceField(queryset=Teacher.objects.filter(is_active=True),widget=forms.Select(
        attrs={'class':'form-control'}),label='강사')
    status = ChoiceField(choices= status_choices,widget=forms.Select(
        attrs={'class': 'form-control'}), label='강의 상태')
    class Meta:
        model = Lecture
        fields = ['name', 'teacher', 'start_date', 'end_date',  'description', 'cost', 'status']
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'placeholder': '강의명을 입력하세요...'
            }),
            'description': Textarea(attrs={
                'class': "form-control",
                'rows': 5,
                'placeholder': '강의에 대한 설명을 입력하세요...'
            }),
            'start_date': DateInput(attrs={
                'format' : '%Y-%m-%d',
                'class': "form-control",
                'placeholder': '개강일',
                'autocomplete': 'off',
            }),
            'end_date': DateInput(attrs={
                'format': '%Y-%m-%d',
                'class': "form-control",
                'placeholder':'종강일',
                'autocomplete': 'off',
            }),
            'cost': NumberInput(attrs={
                'class': "form-control",
                'placeholder': '강의료를 입력하세요.. (예시: 300000)'
            }),

        }

        labels = {
            'name': '강의명',
            'description': '설명',
            'created_at' : '개설일',
            'cost': '수강료',
        }

class CourseTimeCreationForm(ModelForm):
    day_choices=(('1','월요일'),('2','화요일'),('3','수요일'),('4','목요일'),('5','금요일'),('6','토요일'),('0','일요일'))
    day = ChoiceField(choices=day_choices,widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder':'요일'}), label='요일')
    class Meta:
        model=CourseTime
        fields = ['day','start_time', 'end_time']
        widgets = {
            'start_time': TimeInput(attrs={
                'class': "form-control",
                'type': 'time',
                'step': "1800",
                'placeholder': '시작시간',
                'autocomplete': 'off',
            }),
            'end_time': TimeInput(attrs={
                'class': "form-control",
                'type': 'time',
                'step': "1800",
                'autocomplete': 'off',
                'placeholder': '종료시간',
            }),

        }

class CourseRegistrationCreationForm(ModelForm):
    student = ModelChoiceField(queryset=Student.objects.all(),widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder':'학생을 선택해주세요'}), label='학생')
    class Meta:
        model=CourseRegistration
        fields = ['student', 'joined_at']
        widgets = {
            'joined_at': DateInput(attrs={
                'format': '%Y-%m-%d',
                'class': "form-control",
                'placeholder':'수강 시작일',
                'autocomplete': 'off',
            }),
        }