from allauth.account.views import PasswordChangeView, PasswordSetView
from django.http import request
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from django.urls import reverse_lazy

# utillity
class DashboardView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Dashboard"
        greeting['pageview'] = "Dashboards"
        return render(request, 'dashboard/dashboard.html',greeting)

