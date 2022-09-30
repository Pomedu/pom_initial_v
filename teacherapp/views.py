from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from teacherapp.forms import TeacherCreationForm, TeacherUpdateForm
from teacherapp.models import Teacher



def TeacherListView(request):
    context = {}
    context['teacher_list'] = Teacher.objects.all()
    context['heading'] = "강사 목록"
    context['pageview'] = "강사 관리"

    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        teacher = Teacher.objects.get(id=ID)  # So we send the consulting instance
        context['teacher'] = teacher
        return render(request, 'teacherapp/teacher_list.html', context)

    elif request.method == 'POST' and request.POST.get('teacher_delete'):
        teacher = Teacher.objects.get(pk=request.POST.get('teacher_delete'))
        teacher.delete()
        messages.success(request, teacher.name+" 강사("+teacher.phone_number+")를 성공적으로 삭제하였습니다.")
        return redirect('teacherapp:list')

    return render(request,'teacherapp/teacher_list.html',context)

class TeacherCreateView(CreateView):
    model = Teacher
    template_name = 'teacherapp/teacher_create.html'
    form_class = TeacherCreationForm

    def get_context_data(self, **kwargs):
        context = super(TeacherCreateView, self).get_context_data(**kwargs)
        context['heading'] = "강사 생성"
        context['pageview'] = "강사 관리"

        return context

    def get_success_url(self):
        teacher = self.object
        content = "'" + teacher.name + "'" + " 강사를 등록하였습니다."
        messages.success(self.request,content)
        return reverse('teacherapp:list')

    def form_invalid(self, form):
        messages.info(self.request, '이미 존재하는 이름과 전화번호의 강사입니다.')
        return super().form_invalid(form)


class TeacherUpdateView(UpdateView):
    model = Teacher
    template_name = 'teacherapp/teacher_update.html'
    context_object_name = 'target_teacher'
    form_class = TeacherUpdateForm

    def get_context_data(self, **kwargs):
        context = super(TeacherUpdateView, self).get_context_data(**kwargs)
        context['heading'] = " 강사 정보 수정"
        context['pageview'] = "강사 관리"
        return context

    def get_success_url(self):
        teacher = self.object
        content = "'" + teacher.name + "'" + " 강사 정보를 수정하였습니다."
        messages.success(self.request, content)
        return reverse('teacherapp:list')

    def form_invalid(self, form):
        messages.info(self.request, '이미 존재하는 이름과 전화번호의 강사입니다.')
        return super().form_invalid(form)

