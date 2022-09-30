from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, TemplateView


from lectureapp.forms import LectureCreationForm, CourseTimeCreationForm, CourseRegistrationCreationForm
from lectureapp.models import Lecture, CourseRegistration, CourseTime
from studentapp.models import Student
from teacherapp.models import Teacher



def LectureListView(request):
    context = {}
    context['lecture_list'] = Lecture.objects.all()
    context['heading'] = "강의 목록"
    context['pageview'] = "강의 관리"

    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        lecture = Lecture.objects.get(id=ID)  # So we send the consulting instance
        context['lecture'] = lecture
        return render(request, 'lectureapp/lecture_list.html', context)

    elif request.method == 'POST' and request.POST.get('lecture_delete'):
        lecture = Lecture.objects.get(pk=request.POST.get('lecture_delete'))
        lecture.delete()
        messages.success(request, lecture.name+" 강의("+lecture.teacher+")를 성공적으로 삭제하였습니다.")
        return redirect('lectureapp:list')

    return render(request,'lectureapp/lecture_list.html',context)


class LectureGridView(LoginRequiredMixin,ListView):
    template_name = 'lectureapp/lecture_grid.html'
    context_object_name = 'lecture_list'
    paginate_by = 9
    def get_queryset(self):
        if self.request.user.role=='T':
            teacher = Teacher.objects.get(name=self.request.user.name, phone_number=self.request.user.phone_number)
            return Lecture.objects.filter(teacher=teacher)
        elif self.request.user.role=='S':
            student = Student.objects.get(name=self.request.user.name,phone_number=self.request.user.phone_number)
            return Lecture.objects.filter(students__in=student)
        elif self.request.user.role=='A':
            return Lecture.objects.all()

    def get_context_data(self,  **kwargs):
        context = super(LectureGridView, self).get_context_data(**kwargs)
        context['heading'] = "강의 목록"
        context['pageview'] = "강의"
        paginator = context['paginator']
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context



class LectureCreateView(LoginRequiredMixin,TemplateView):

    template_name = 'lectureapp/lecture_create.html'

    def get_context_data(self, **kwargs):
        context = super(LectureCreateView, self).get_context_data(**kwargs)
        context['heading'] = "강의 생성"
        context['pageview'] = "강의 관리"
        context['lecture_form'] = LectureCreationForm()
        context['coursetime_form'] = CourseTimeCreationForm()
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request):
        lectureform = LectureCreationForm(request.POST)
        if lectureform.is_valid():
            lecture = lectureform.save()
            coursetime_num = 0
            while True:
                try:
                    day = request.POST.get(f'coursetime[{coursetime_num}][day]')
                    start_time = request.POST.get(f'coursetime[{coursetime_num}][start_time]')
                    end_time = request.POST.get(f'coursetime[{coursetime_num}][end_time]')
                    coursetime = CourseTime.objects.create(lecture=lecture, start_time=start_time, end_time=end_time, day=day)
                    coursetime_num += 1
                except:
                    break
            messages.success(request, "강의를 성공적으로 등록하였습니다.")
            return redirect('lectureapp:lecture_list')
        else:
            messages.success(request, "강의 등록에 실패하였습니다")
            return render(request, self.template_name, self.get_context_data())

def LectureUpdateView(request, pk):
    context = {}
    context['heading'] = "강의 정보 수정"
    context['pageview'] = "강의 관리"
    lecture = Lecture.objects.get(pk=pk)
    coursetime_list = CourseTime.objects.filter(lecture=lecture)
    context['lecture'] = lecture
    context['coursetime_list'] = coursetime_list
    context['teacher_list'] = Teacher.objects.filter(is_active=True)
    context['pk'] =  pk

    if request.method=='POST' and request.POST.get('lecture_update'):
        try:
            lecture.name = request.POST.get('name')
            lecture.teacher = Teacher.objects.get(name=request.POST.get('teacher'))
            lecture.start_date = request.POST.get('start_date')
            lecture.end_date = request.POST.get('end_date')
            lecture.description = request.POST.get('description')
            lecture.cost = request.POST.get('cost')
            lecture.status = request.POST.get('status')
            # 기존 강의 시간 삭제
            for coursetime in coursetime_list:
                coursetime.delete()
            coursetime_num = 0
            # 새 강의 시간 등록
            while True:
                try:
                    day = request.POST.get(f'coursetime[{coursetime_num}][day]')
                    start_time = request.POST.get(f'coursetime[{coursetime_num}][start_time]')
                    end_time = request.POST.get(f'coursetime[{coursetime_num}][end_time]')
                    CourseTime.objects.create(lecture=lecture, start_time=start_time, end_time=end_time,day=day)
                    coursetime_num += 1
                except:
                    break
            messages.success(request, "강의를 성공적으로 수정하였습니다.")
            return redirect('lectureapp:lecture_list')
        except:
            messages.success(request, "강의 정보 수정에 실패하였습니다")
            return render(request, "lectureapp/lecture_update.html", context)


    return render(request, 'lectureapp/lecture_update.html', context)



class LectureDetailView(DetailView):
    model = Lecture
    context_object_name = 'target_lecture'
    template_name = 'lectureapp/lecture_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LectureDetailView, self).get_context_data(**kwargs)
        context['heading'] = "강의 상세"
        context['pageview'] = "강의 관리"
        return context


def CourseRegistrationCreateView(request):
    context = {}
    if request.user.role == 'A':
        context['teacher_list'] = Teacher.objects.all()
    elif request.user.role == 'T':
        teacher = Teacher.objects.get(name=request.user.name, phone_number=request.user.phone_number)
        context['teacher'] = teacher
    context['heading'] = "수강 등록"
    context['pageview'] = "강의 관리"

    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        lecture = Lecture.objects.get(id=ID)  # So we send the consulting instance
        context['lecture'] = lecture
        return render(request, 'lectureapp/courseregistration_select_lecture.html', context)

    if request.method == 'POST' and request.POST.get('selected_lecture'):
        context['lecture'] = Lecture.objects.get(id=request.POST.get('selected_lecture'))
        context['student_list'] = Student.objects.all()
        return render(request, 'lectureapp/courseregistration_select_student.html', context)

    return render(request, 'lectureapp/courseregistration_select_lecture.html', context)


def CourseRegistrationCreateView_2(request):
    context = {}
    context['student_list'] = Student.objects.all()
    context['heading'] = "수강 등록"
    context['pageview'] = "강의 관리"

    if request.method == 'POST':
        # validation(강의 정보 확인)
        try:
            lecture = Lecture.objects.get(id=request.POST.get('selected_lecture'))
        except:
            messages.warning(request, "강의 정보가 소실되었습니다. 수강등록을 다시 진행해주세요")
            context = {}
            if request.user.role == 'A':
                context['teacher_list'] = Teacher.objects.all()
            elif request.user.role == 'T':
                teacher = Teacher.objects.get(name=request.user.name, phone_number=request.user.phone_number)
                context['teacher'] = teacher
            context['heading'] = "수강 등록"
            context['pageview'] = "강의 관리"
            return redirect('lectureapp:courseregistration_list')

        student_ids = request.POST.getlist('student_id[]')
        joined_at_list = request.POST.getlist('joined_at[]')
        #validation(입력 정보 확인)
        if len(student_ids) != len(set(student_ids)):
            messages.warning(request, "동일한 학생 정보가 중복으로 입력되었습니다. 다시 입력해주세요")
            context['lecture'] = Lecture.objects.get(id=request.POST.get('selected_lecture'))
            return redirect('lectureapp:courseregistration_list')

        for i in range(len(student_ids)):
            try:
                CourseRegistration.objects.create(lecture=lecture,student=Student.objects.get(id=student_ids[i]),joined_at=joined_at_list[i])
            except ValidationError:
                messages.warning(request, "수강일을 제대로 입력하지 않았습니다. 다시 확인해주세요")
                return redirect('lectureapp:courseregistration_list')
            except IntegrityError:
                messages.warning(request, "이미 등록된 수강정보가 있습니다. 확인 후 등록해주세요")
                return redirect('lectureapp:courseregistration_list')
        messages.success(request, "수강 등록이 완료되었습니다")
        return redirect('lectureapp:courseregistration_list')

    return render(request, 'lectureapp/courseregistration_select_student.html', context)


class CourseRegistrationListView(TemplateView):
    template_name = 'lectureapp/courseregistration_list.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        if self.request.user.role=='A':
            context['teacher_list'] = Teacher.objects.all()
        elif self.request.user.role=='T':
            teacher = Teacher.objects.get(name=self.request.user.name, phone_number=self.request.user.phone_number)
            context['teacher'] = teacher
        context['heading'] = "수강 목록"
        context['pageview'] = "수강 관리"
        return context


    def post(self, request):
        context= super().get_context_data()
        if request.is_ajax() and request.POST.get('callcourseregistration'):
            ID = request.POST.get('callcourseregistration')
            lecture = Lecture.objects.get(id=ID)  # So we send the consulting instance
            courseregistration_list = CourseRegistration.objects.filter(lecture=lecture)
            if not courseregistration_list:
                messages.info(request, "해당 수업에 등록된 수강생이 없습니다")
                redirect('lectureapp:courseregistration_list')
            else:
                context['courseregistration_list'] = courseregistration_list
                return render(request, 'lectureapp/courseregistration_list.html', context)
        if request.is_ajax() and request.POST.get('delete_id'):
            print('성공')
            ID = request.POST.get('delete_id')
            courseregistration = CourseRegistration.objects.get(id=ID)  # So we send the consulting instance
            context['courseregistration'] = courseregistration
            return render(request, 'lectureapp/courseregistration_list.html', context)

        if request.POST.get('courseregistration_delete'):
            courseregistration = CourseRegistration.objects.get(pk=request.POST.get('courseregistration_delete'))
            courseregistration.delete()
            messages.success(request, courseregistration.student.name + " 학생의 '" + courseregistration.lecture.name + "'강의에 대한 수강정보를 성공적으로 삭제하였습니다.")
            return redirect('lectureapp:courseregistration_list')

        return render(request, 'lectureapp/courseregistration_list.html', context)

class LectureTimetableView(TemplateView):
    template_name = 'lectureapp/lecture_timetable.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['heading'] = "강의 시간표"
        context['pageview'] = "강의 관리"
        context['coursetime_list'] = CourseTime.objects.all()
        context['lecture_list'] = Lecture.objects.all()
        return context

class LectureTimetableView_Ongoing(TemplateView):
    template_name = 'lectureapp/lecture_timetable.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['heading'] = "나의 시간표"
        context['pageview'] = "My Space"

        if self.request.user.role == 'T':
            teacher = Teacher.objects.get(name=self.request.user.name, phone_number=self.request.user.phone_number)
            context['coursetime_list'] = CourseTime.objects.filter(lecture__teacher=teacher)
            context['lecture_list'] = Lecture.objects.filter(teacher=teacher)
        elif self.request.user.role == 'S':
            student = Student.objects.get(name=self.request.user.name, phone_number=self.request.user.phone_number)
            context['coursetime_list'] = CourseTime.objects.filter(lecture__students__in=student)
            context['lecture_list'] = Lecture.objects.filter(students__in=student)

        return context
