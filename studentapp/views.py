from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from studentapp.forms import StudentCreationForm
from studentapp.models import Student


def StudentListView(request):
    context = {}
    context['student_list'] = Student.objects.all()
    context['heading'] = "학생 목록"
    context['pageview'] = "학생 관리"

    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        student = Student.objects.get(id=ID)  # So we send the consulting instance
        context['student'] = student
        return render(request, 'studentapp/student_list.html', context)

    elif request.method == 'POST' and request.POST.get('student_delete'):
        student = Student.objects.get(pk=request.POST.get('student_delete'))
        student.delete()
        messages.success(request, student.name+" 학생("+student.phone_number+")을 성공적으로 삭제하였습니다.")
        return redirect('studentapp:list')

    return render(request,'studentapp/student_list.html',context)

class StudentCreateView(CreateView):
    model = Student
    template_name = 'studentapp/student_create.html'
    form_class = StudentCreationForm

    def get_context_data(self, **kwargs):
        context = super(StudentCreateView, self).get_context_data(**kwargs)
        context['heading'] = "학생 생성"
        context['pageview'] = "학생 관리"

        return context

    def get_success_url(self):
        student = self.object
        content = "'" + student.name + "'" + " 학생을 등록하였습니다."
        messages.success(self.request,content)
        return reverse('studentapp:list')

    def form_invalid(self, form):
        messages.info(self.request, '이미 존재하는 이름과 전화번호의 학생입니다.')
        return super().form_invalid(form)


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'studentapp/student_update.html'
    context_object_name = 'target_student'
    form_class = StudentCreationForm

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['heading'] = " 학생 정보 수정"
        context['pageview'] = "학생 관리"
        return context

    def get_success_url(self):
        student = self.object
        content = "'" + student.name + "'" + " 학생 정보를 수정하였습니다."
        messages.success(self.request, content)
        return reverse('studentapp:list')

    def form_invalid(self, form):
        messages.info(self.request, '이미 존재하는 이름과 전화번호의 학생입니다.')
        return super().form_invalid(form)
