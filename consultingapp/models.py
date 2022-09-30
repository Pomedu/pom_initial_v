from django.db import models

# Create your models here.
from django.core.validators import RegexValidator

from accountapp.models import User
from teacherapp.models import Teacher


class Consulting(models.Model):
    phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',message="올바른 전화번호 양식을 입력해주세요 ex)010-0000-0000")
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
    in_charge_A = models.ForeignKey(User,limit_choices_to={'role':'A'}, on_delete=models.SET_NULL, related_name='consultings', null=True, blank=True)
    in_charge_T = models.ForeignKey(Teacher, on_delete=models.SET_NULL, related_name='consultings', null=True,blank=True)
    client_name = models.CharField(max_length=100, null=False)
    client_phone_number = models.CharField(validators=[phoneNumberRegex], max_length=20, null=False)
    client_school = models.CharField(max_length=20, null=True)
    client_grade = models.CharField(max_length=20, choices=grade_choices)
    content = models.TextField(null=True,blank=True)
    status =  models.CharField(max_length=20, choices=status_choices)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
