import re

from allauth.account import app_settings
from allauth.account.utils import complete_signup
from allauth.account.views import PasswordChangeView, PasswordSetView
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView

from accountapp.forms import UserRegistrationForm
from accountapp.models import User, Teacher, Student

from allauth.account.views import SignupView


class TeacherRegistrationView(SignupView):
    form_class = UserRegistrationForm
    template_name = 'accountapp/signup_teacher.html'

    def form_valid(self, form):
        role = self.request.POST['role']
        REGEX_PHONE_NUMBER = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$'
        phone_number = re.sub(r"[^0-9]", "", self.request.POST['phone_number'])
        role = self.request.POST['role']
        self.user = form.save(self.request)
        self.user.phone_number = phone_number
        self.user.role = role
        self.user.save()
        try:
            return complete_signup(
                self.request,
                self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url(),
            )
        except ImmediateHttpResponse as e:
            return e.response

class StudentRegistrationView(SignupView):
    form_class = UserRegistrationForm
    template_name = 'accountapp/signup_student.html'

    def form_valid(self, form):
        phone_number = re.sub(r"[^0-9]", "", self.request.POST['phone_number'])
        role = self.request.POST['role']
        self.user = form.save(self.request)
        self.user.phone_number = phone_number
        self.user.role = role
        self.user.save()
        try:
            return complete_signup(
                self.request,
                self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url(),
            )
        except ImmediateHttpResponse as e:
            return e.response

# @login_required
# @transaction.atomic
# def update_information(request, pk):
#     if request.method == 'POST':
#         phone_num = re.sub(r"[^0-9]", "", request.POST['phone_num'])
#         user = request.user
#         user.name = request.POST['name']
#         user.phone_num = phone_num
#         user.
#         try :
#             profile.profile_photo = request.FILES['profile_photo']
#             profile.save()
#         except:
#             profile.save()
#         messages.success(request, '개인정보가 성공적으로 업데이트 되었습니다!')
#         return redirect('profileapp:detail',request.user.profile.pk)
#     else:
#         profile = Profile.objects.get(pk=pk)
#         return render(request,"profileapp/update.html", {'target_profile': profile })
#
class AccountDetailView(DetailView):
    model = User
    template_name = 'accountapp/detail.html'
    context_object_name = 'target_user'


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('dashboard')

class MyPasswordSetView(LoginRequiredMixin, PasswordSetView):
    success_url = reverse_lazy('dashboard')

