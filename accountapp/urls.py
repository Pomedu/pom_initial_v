from django.contrib.auth.decorators import login_required
from django.urls import path

from accountapp.views import AccountDetailView, MyPasswordSetView, MyPasswordChangeView, TeacherRegistrationView, \
    StudentRegistrationView

app_name = 'accountapp'

urlpatterns = [
    # Profile
    path('detail/<int:pk>',AccountDetailView.as_view(), name='detail'),
    # Custum change password done page redirect
    path('password/change/', login_required(MyPasswordChangeView.as_view()), name="account_change_password"),
    # Custum set password done page redirect
    path('password/set/', login_required(MyPasswordSetView.as_view()), name="account_set_password"),
    # Resgistration
    path('signup_teacher/',TeacherRegistrationView.as_view(),name='signup_teacher'),
    path('signup_student/',StudentRegistrationView.as_view(),name='signup_student'),
    #UserList
]