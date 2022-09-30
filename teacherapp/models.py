from django.core.validators import RegexValidator
from django.utils.html import escape
from django.utils.safestring import mark_safe

from django.db import models

# Create your models here.

phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
                                  message="올바른 전화번호 양식을 입력해주세요 ex)010-0000-0000")

class Subject(models.Model):
    subject_choices = (
        ('kor', '국어'),
        ('math', '수학'),
        ('eng', '영어'),
        ('sci', '과학'),
        ('soc', '사회'),
        ('ess', '논술')
    )
    name = models.CharField(max_length=20, choices=subject_choices, null=False)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class Teacher(models.Model):
    name = models.CharField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=20, null=False)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL, related_name='teachers')
    created_at = models.DateField(auto_now_add=True, null=False)
    is_active = models.BooleanField(default=True)
    account_linked = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name','phone_number'],
                name='unique_teacher'
            )
        ]