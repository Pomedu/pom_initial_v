from django.db import models

from studentapp.models import Student
from teacherapp.models import Teacher


class Lecture(models.Model):
    status_choices = (
        ('P', '대기'),
        ('O', '진행중'),
        ('F', '종강'),
    )
    name = models.CharField(max_length=100, null=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, related_name='lectures', null=True)
    description = models.TextField(null=True,blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=status_choices, null=False)
    cost = models.IntegerField(null=False)
    students = models.ManyToManyField(Student, through='CourseRegistration', related_name='lectures')
    def __str__(self):
        return self.name

class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='course')
    joined_at = models.DateField(null=False)
    created_at = models.DateField(auto_now_add=True, null=False)
    class Meta:
        unique_together = ('student', 'lecture')

class CourseTime(models.Model):
    day_choices = (('1', '월'), ('2', '화'), ('3', '수'), ('4', '목'), ('5', '금'), ('6', '토'), ('0  ', '일'))
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='time')
    day = models.CharField(max_length=3,choices=day_choices,null=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
