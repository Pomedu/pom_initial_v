from django.contrib.auth.decorators import login_required
from django.urls import path

from lectureapp.views import LectureListView, LectureCreateView, LectureDetailView, LectureTimetableView, \
    CourseRegistrationCreateView, CourseRegistrationListView, LectureTimetableView_Ongoing, \
    LectureGridView, LectureUpdateView, CourseRegistrationCreateView_2

app_name = 'lectureapp'

urlpatterns = [
    path('list',LectureListView, name='lecture_list'),
    path('list/ongoing',LectureGridView.as_view(), name='lecture_grid'),
    path('create/lecture',LectureCreateView.as_view(), name='lecture_create'),
    path('detail/<int:pk>',LectureDetailView.as_view(), name='lecture_detail'),
    path('update/<int:pk>',LectureUpdateView, name='lecture_update'),
    path('timetable/',LectureTimetableView.as_view(), name='timetable'),
    path('myspace/timetable',LectureTimetableView_Ongoing.as_view(), name='timetable_ongoing'),
    path('create/courseregistration',CourseRegistrationCreateView, name='courseregistration_create'),
    path('create/courseregistration_2', CourseRegistrationCreateView_2, name='courseregistration_create_2'),
    path('list/courseregistration',CourseRegistrationListView.as_view(), name='courseregistration_list'),

]