"""pom_LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import TemplateView

from pom_LMS import settings
from pom_LMS.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dashboards View
    path('', DashboardView.as_view(), name='dashboard'),

    # Allauth
    path('account/', include('allauth.urls')),
    path('auth-logout/', TemplateView.as_view(template_name="account/logout-success.html"), name='pages-logout'),
    path('auth-lockscreen/', TemplateView.as_view(template_name="account/lock-screen.html"), name='pages-lockscreen'),
    # Profile
    path('accounts/', include('accountapp.urls')),
    # Lecture
    path('lectures/', include('lectureapp.urls')),
    # Student
    path('students/', include('studentapp.urls')),
    # Teacher
    path('teachers/', include('teacherapp.urls')),
    # Consulting
    path('consultings/', include('consultingapp.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)