

from allauth.account.signals import email_confirmed
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.utils import timezone

from studentapp.models import Student
from teacherapp.models import Teacher


class UserManager(BaseUserManager):

    def _create_user(self, email, name, password, is_admin, is_superuser, role, phone_number):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            is_admin=is_admin,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            role=role,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password, role, phone_number):
        return self._create_user(email, name, password, False, False, role, phone_number)

    def create_superuser(self, email, name, password,  role, phone_number):
        user = self._create_user(email, name, password, True, True,  role, phone_number)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
                                      message="올바른 전화번호 양식을 입력해주세요 ex)010-0000-0000")
    USER_ROLES = (
        ('A', 'Administrator'),
        ('T', 'Teacher'),
        ('S', 'Student'),
    )

    role = models.CharField(max_length=1, blank=False, choices=USER_ROLES)
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=20, null=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name','role','phone_number']

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = User.objects.get(email=email_address.email)
    user.is_active = True
    if user.role == "T":
        try:
            teacher = Teacher.objects.get(name=user.name, phone_number=user.phone_number)
            teacher.account_linked = True
            teacher.save()
        except Teacher.DoesNotExist:
            pass

    elif user.role == "S":
        try:
            student = Student.objects.get(name=user.name, phone_number=user.phone_number)
            student.account_linked = True
            student.save()
        except Student.DoesNotExist:
            pass

    elif user.role == "A":
        user.is_admin = True
        user.save()

