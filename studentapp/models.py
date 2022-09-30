from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
                                  message="올바른 전화번호 양식을 입력해주세요 ex)010-0000-0000")

class Student(models.Model):

    name = models.CharField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=20, null=False)
    phone_number_P =  models.CharField(validators=[phoneNumberRegex], max_length=20, null=True, blank=True)
    school = models.CharField(max_length=20, null=True)
    created_at = models.DateField(auto_now_add=True, null=False)
    account_linked = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name','phone_number'],
                name='unique_student'
            )
        ]