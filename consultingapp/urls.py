from django.contrib.auth.decorators import login_required
from django.urls import path

from consultingapp.views import ConsultingListView, ConsultingCreateView, ConsultingUpdateView

app_name = 'consultingapp'

urlpatterns = [
    path('consulting_list/',ConsultingListView, name='consulting_list'),
    path('consulting_create/',ConsultingCreateView.as_view(), name='consulting_create'),
    path('consulting_update/<int:pk>',ConsultingUpdateView.as_view(), name='consulting_update'),
]