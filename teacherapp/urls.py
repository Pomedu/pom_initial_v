from django.contrib.auth.decorators import login_required
from django.urls import path

from teacherapp.views import TeacherListView, TeacherCreateView, TeacherUpdateView

app_name = 'teacherapp'

urlpatterns = [
    path('list/',TeacherListView,name='list'),
    path('create/',TeacherCreateView.as_view(),name='create'),
    path('update/<int:pk>',TeacherUpdateView.as_view(),name='update'),
]