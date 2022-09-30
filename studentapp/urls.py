from django.contrib.auth.decorators import login_required
from django.urls import path

from studentapp.views import StudentListView, StudentCreateView, StudentUpdateView

app_name = 'studentapp'

urlpatterns = [
    path('list/',StudentListView,name='list'),
    path('create/',StudentCreateView.as_view(),name='create'),
    path('update/<int:pk>',StudentUpdateView.as_view(),name='update'),

]