import re

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from consultingapp.forms import ConsultingCreationForm
from consultingapp.models import Consulting


def ConsultingListView(request):
    context = {}
    context['pending_list'] = Consulting.objects.filter(Q(status="P")|Q(status="N"))
    context['completed_list'] = Consulting.objects.filter(status="F")
    context['heading'] = "상담 관리"
    context['pageview'] = "상담 목록"

    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        consulting = Consulting.objects.get(id=ID)  # So we send the consulting instance
        context['consulting'] = consulting
        return render(request, 'consultingapp/consulting_list.html', context)

    elif request.method == 'POST' and request.POST.get('consulting_delete'):
        consulting = Consulting.objects.get(pk=request.POST.get('consulting_delete'))
        consulting.delete()
        messages.success(request, "상담("+consulting.client_phone_number+")을 성공적으로 삭제하였습니다.")
        return redirect('consultingapp:consulting_list')

    return render(request,'consultingapp/consulting_list.html',context)


class ConsultingCreateView(LoginRequiredMixin,CreateView):
    model = Consulting
    template_name = 'consultingapp/consulting_create.html'
    form_class = ConsultingCreationForm

    def get_context_data(self, **kwargs):
        context = super(ConsultingCreateView, self).get_context_data(**kwargs)
        context['heading'] = "상담 생성"
        context['pageview'] = "상담 관리"
        return context

    def form_valid(self, form):
        phone_number = re.sub(r"[^0-9]", "", self.request.POST['client_phone_number'])
        consulting = form.save(self.request)
        consulting.client_phone_number = phone_number
        consulting.save()
        return super().form_valid(form)

    def get_success_url(self):
        consulting = self.object
        # event = Event(actor=self.request.user, content=content)
        # event.save()
        messages.success(self.request, "상담(" + consulting.client_phone_number + ")을 등록하였습니다.")
        return reverse('consultingapp:consulting_list')

class ConsultingUpdateView(UpdateView):
    model = Consulting
    template_name = 'consultingapp/consulting_update.html'
    context_object_name = 'target_consulting'
    form_class = ConsultingCreationForm

    def get_context_data(self, **kwargs):
        context = super(ConsultingUpdateView, self).get_context_data(**kwargs)
        context['heading'] = "상담 수정"
        context['pageview'] = "상담 관리"
        return context

    def form_valid(self, form):
        phone_number = re.sub(r"[^0-9]", "", self.request.POST['client_phone_number'])
        consulting = form.save(self.request)
        consulting.client_phone_number = phone_number
        consulting.save()
        return super().form_valid(form)

    def get_success_url(self):
        consulting = self.object
        # event = Event(actor=self.request.user, content=content)
        # event.save()
        messages.success(self.request, "상담(" + consulting.client_phone_number + ")을 수정하였습니다.")
        return reverse('consultingapp:consulting_list')