from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse

from Arrangementapp.models import Login
from Arrangementapp.serializer import *
from .forms import Subsembranchform
from.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED

# Create your views here.
class LoginPage(View):
    def get(self,request):
        return render(request,"login.html")
    def post(self,request):
       
        try:
            #    print(request.POST['username'])
            username=request.POST['username']
            password=request.POST['password']
            obj=Login.objects.get(Username=username,Password=password)
            if(obj.Usertype=='admin'):
                return render(request, "base.html")
            else:
                return HttpResponse("'''<script>alert('Inavlid username and password');window.location.href='/'</script>'''")

        except Login.DoesNotExist:
            return HttpResponse("'''<script>alert('Inavlid username and password');window.location='/'</script>'''")

       


#////////////////////////////////ADMIN////////////////////////

class Viewsub(View):
    def get(self, request):
        semester_instances = Semester.objects.all()
        branch_instances = Branch.objects.all()
        subject_instances =Subject.objects.all()
        return render(request, 'Sem.html', {'branch_instances': branch_instances, 'semester_instances': semester_instances,'subject_instances':subject_instances})
    def post(self,request):
        branch = request.POST['branch']
        semester = request.POST['semester']
        print(branch)
        print(semester)
        semester_instances = Semester.objects.all()
        branch_instances = Branch.objects.all()
        subject_instances = Subject.objects.filter(branch=branch, semester=semester).all()
        print(subject_instances)
        return render(request, 'Sem.html',
                      {'subject_instances': subject_instances, 'semester_instances': semester_instances,
                       'branch_instances': branch_instances})



class Addsub(View):
    template_name = 'addsubject.html'  # Replace 'your_template.html' with your actual template path
    success_url = '/viewsub/'  # Change the URL as needed

    def get(self, request):
        semester_instances = Semester.objects.all()
        branch_instances = Branch.objects.all()
 # Render the form
        return render(request, self.template_name,{'semester_instances':semester_instances,'branch_instances':branch_instances})

    def post(self, request):
        # Get the submitted form data
        branches = request.POST.getlist('branch')
        semesters = request.POST.getlist('semester')
        subjects = request.POST.getlist('subjectname')
        subject_codes = request.POST.getlist('subjectcode')
        print(branches)
        print(semesters)
        print(subjects)
        print(subject_codes)

        # Iterate through the submitted data and save subjects
        for branch, semester, subject, subject_code in zip(branches, semesters, subjects, subject_codes):
            # Create a new Subject object
            print(branch)
            new_subject = Subject(
                branch = Branch.objects.get(id=branch),
                semester =Semester.objects.get(id=semester),

                subjectname=subject,
                subjectcode=subject_code,
                  # Assuming subjects are active by default
            )
            # Save the new subject
            new_subject.save()
# Redirect to the success URL
        return redirect(self.success_url)
class Editsub(View):
    def get(self,request,id):
        semester_instances = Semester.objects.all()
        branch_instances = Branch.objects.all()
        subject_instances = Subject.objects.filter(id=id).first()
        return render(request, 'editSub.html', {'subject_instances': subject_instances,'branch_instances':branch_instances,'semester_instances':semester_instances})
    def post(self,request,id):
        print("hhhh")
        subject_instances = Subject.objects.filter(id=id).first()
        form=Subsembranchform(request.POST,instance=subject_instances)
        if form.is_valid():
            print("ccccccc")
            form.save()
            return redirect('viewsub')
class Deletesub(View):
    def get(self,request,id):
        subject_instances = Subject.objects.filter(id=id).first()
        subject_instances.delete()
        return redirect('/viewsub')
    
class View_exam(View):
    def get(self,request):
        exam_instances=ExamDetails.objects.all()
        return render(request, 'exam.html',{'exam_instances':exam_instances})
    def post(self,request):
        exam_date=request.POST['exam_date']
        print(exam_date)
        exam_instances=ExamDetails.objects.filter(exam_date=exam_date).all()
        return render(request, 'exam.html', {'exam_instances':exam_instances})
class Add_exam(View):
    def get(self,request):
        semester_instances = Semester.objects.all()
        branch_instances = Branch.objects.all()
        subject_instances = Subject.objects.all()

        return render(request, 'addexam.html',{'semester_instances':semester_instances,'branch_instances':branch_instances,'subject_instances':subject_instances})


    def post(self, request):
        # Retrieve form data
        exam_names = request.POST.getlist('exam_datas')
        branch_datas=request.POST.getlist('branch_names')
        semester_datas=request.POST.getlist('semester_names')
        subject_ids = request.POST.getlist('subjects')
        exam_dates = request.POST['exam_date']
        exam_times = request.POST['exam_time']

        student_counts = request.POST.getlist('total_students')  # Assuming this is the number of students for each exam
        print(exam_names)
        print(branch_datas)
        print(semester_datas)
        print(exam_times)
        print(exam_dates)
        print(subject_ids)
        print(student_counts)
        # Iterate through the form data to create and save ExamDetails instances
        for exam_name, subject_id, student_count in zip(exam_names,subject_ids, student_counts):
            exam_detail = ExamDetails(
                exam_name=exam_name,
                exam_subject=Subject.objects.get(pk=subject_id),
                exam_date=exam_dates,
                exam_time=exam_times,
                no_of_students=student_count,
                # Add any other fields related to the exam details
                # is_active=True  # Assuming you want to set it as active by default
            )
            exam_detail.save()

        # Redirect to a success page or any other page
        return redirect('/viewexam/')
class Deleteexam(View):
    def get(self, request, id):
        # Retrieve the subject instance
        exam_instance = ExamDetails.objects.filter(id=id).first()

        # Check if subject exists and is active
        if exam_instance:
            # Perform hard delete
            exam_instance.delete()

        return redirect('/viewexam/')
@csrf_exempt
def fetch_subjects(request):
    if request.method == 'GET':
        branch_id = request.GET.get('branch')
        semester_id = request.GET.get('semester')

        # Query subjects based on the selected branch and semester
        subjects = Subject.objects.filter(branch_id=branch_id, semester_id=semester_id)
        studentcount = Studentprofile.objects.filter(branch_id=branch_id, semester_id=semester_id).count()
        print(studentcount)
        # Serialize queryset into JSON format
        subjects_data = [{'id': subject.id, 'subjectname': subject.subjectname} for subject in subjects]

        # Create JSON response data including subjects and student count
        response_data = {
            'subjects': subjects_data,
            'studentcount': studentcount
        }

        return JsonResponse(response_data, safe=False)
    
    #classroom
class ViewClassroom(View):
    def get(self,request):
        classroom_instances = Classroom.objects.filter(is_active=True).all()
        return render(request, 'class.html',{'classroom_instances':classroom_instances})

class AddClassroom(View):
    def get(self, request):
        # Render the form template
        return render(request, 'addclass.html')

    def post(self, request):
        hall_data = request.POST.getlist('hallno')
        capacity_data = request.POST.getlist('capacity')
        columns_data = request.POST.getlist('columns')

        for hallno, capacity, columns in zip(hall_data, capacity_data, columns_data):
            examhall = Classroom(
                hallno=hallno,
                capacity=int(capacity),
                columns=int(columns),
                is_active=True
            )
            examhall.save()


        # Redirect to a success page or any other page
        return redirect('viewclassroom')


class Deleteclassroom(View):
    def get(self, request, id):
        # Retrieve the subject instance
        classroom_instance = Classroom.objects.filter(id=id, is_active=True).first()

        # Check if subject exists and is active
        if classroom_instance:
            # Perform hard delete
            classroom_instance.delete()

        return redirect('viewclassroom')
    
class Allocatestaff(View):
    def get(self,request):
        ex_instances=ExamDetails.objects.filter().all()
        # up_instances=Userprofile.objects.filter(user_type='STAFF').all()
        st_instances=Staff_Profile.objects.filter().all()
        return render(request,'allocatestaff.html',{'ex_instances':ex_instances,'st_instances':st_instances})
    def post(self,request):
        exams = request.POST.getlist('exams')
        exam_halls= request.POST.getlist('exam_hall')
        teachers = request.POST.getlist('teacher')

        print(exams)
        print(exam_halls)
        print(teachers)


        # Iterate through the submitted data and save subjects
        for exam, examhall, teacher, in zip(exams, exam_halls, teachers):
            # Create a new Subject object

            new_seating = Teacherseatingarrangement(
                exam=ExamDetails.objects.get(id=exam),
                exam_hall=Classroom.objects.get(hallno=examhall),
                teacher=Login.objects.get(id=teacher),
                # Assuming subjects are active by default
            )
            # Save the new subject
            new_seating.save()

        # Redirect to the success URL
        return redirect('/allocateviewstaff')


class Allocateviewstaff(View):
    def get(self, request):
        ts_instances = Teacherseatingarrangement.objects.filter().all()

        return render(request, 'allocateviewstaff.html', {'ts_instances': ts_instances})
class Allocatedeletestaff(View):
    def get(self, request,id):
        ts_instances = Teacherseatingarrangement.objects.filter(id=id).first()
        ts_instances.delete()
        return redirect('/allocateviewstaff/')

        return render(request, 'allocateviewstaff.html', {'ts_instances': ts_instances})
    

class ViewStaff(View):
    def get(self, request):
        # Render the form template
        staff_instances=Staff_Profile.objects.all()
        return render(request, 'staff.html',{'staff_instances':staff_instances})
    
class AddStaff(View):
    def get(self, request):
        # Render the form template
        subject_instances=Subject.objects.all()
        return render(request, 'addstaff.html',{'subject_instances':subject_instances})

    def post(self, request):
        subject_data = request.POST.getlist('subject')
        staff_id_data = request.POST.getlist('staff_id')
        first_name_data = request.POST.getlist('first_name')
        email_data=request.POST.getlist('email')

        for subject, staff_id, first_name,email in zip(subject_data, staff_id_data, first_name_data,email_data):
            user =Login.objects.create(
                Username=staff_id,
                Password=staff_id,
                first_name=first_name_data,# Assuming staff_id is used as username
                Usertype="STAFF"
            )
            staff_profile = Staff_Profile.objects.create(

                user=user,
                name=first_name_data,
                staff_id=staff_id,
                subject=Subject.objects.get(id=subject)
            )
            staff_profile.save()


        # Redirect to a success page or any other page
        return redirect('/viewstaff/')


class Deletestaff(View):
    def get(self, request, id):
        # Retrieve the subject instance
        staff_instance = Staff_Profile.objects.filter(id=id, is_active=True).first()
        user_instance=Login.objects.filter(pk=staff_instance.user.id).first()
        # Check if subject exists and is active
        if user_instance:
            # Perform hard delete
            user_instance.delete()

        return redirect('/viewstaff/')  
    

    #////////////////////////////////////////////// STUDENT API ///////////////////////////////////////////////
    
    
class UserRegAPI(APIView):
    def post(self, request):
        print("###############",request.data)
        user_serial = UserSerializer(data=request.data)
        Login_serial = Loginserializer(data=request.data)
        data_valid = user_serial.is_valid()
        Login_valid = Login_serial.is_valid()

        if data_valid and Login_valid:
            print("&&&&&&&&&&&&&&&&")
            password = request.data['password']
            login_profile = Login_serial.save(user_type='USER', password=password)
            user_serial.save(Login=login_profile)
            return Response(user_serial.data, status=status.HTTP_201_CREATED)
        return Response({'login_error': Login_serial.errors if not Login_valid else None,
                            'user_error': user_serial.errors if not data_valid else None}, status=status.HTTP_400_BAD_REQUEST)

class LoginPageAPI(APIView):
    def post(self, request):
        print("################API###############")
        response_dict = {}

        # Get data from the request
        username = request.data.get("username")
        password = request.data.get("password")

        # Validate input
        if not username or not password:
            response_dict["message"] = "failed"
            return Response(response_dict, status=HTTP_400_BAD_REQUEST)

        # Fetch the user from LoginTable
        t_user = Login.objects.filter(Username=username).first()

        if not t_user:
            response_dict["message"] = "failed"
            return Response(response_dict, status=HTTP_401_UNAUTHORIZED)

        # # Check password using check_password
        # if not check_password(password, t_user.password):
        #     response_dict["message"] = "failed"
        #     return Response(response_dict, status=HTTP_401_UNAUTHORIZED)

        # Successful login response
        response_dict["message"] = "success"
        response_dict["login_id"] = t_user.id
        response_dict["usertype"] = t_user.Usertype

        return Response(response_dict, status=HTTP_200_OK)


class ViewExamHallAPI(APIView):
    def get(self,request):
        examinationhall  = Seating_Arrangement.objects.all()
        examinationhall_serializer = ExaminationHallserializer(examinationhall, many = True)
        return Response(examinationhall_serializer.data) 

class ViewExamScheduleAPI(APIView):
    def get(self,request):
        examschedule  = ExamDetails.objects.all()
        examschedule_serializer = ExamScheduleserializer(examschedule, many = True)
        return Response(examschedule_serializer.data) 

class ViewExamNotificationAPI(APIView):
    def get(self,request):
        notification  = ExamNotification.objects.all()
        examnotification_serializer = ExamNotificationserializer(notification, many = True)
        return Response(examnotification_serializer.data)    
    
class ViewReplyAPI(APIView):
    def get(self,request):
        reply  = Complaint.objects.all()
        reply_serializer = Replyserializer(reply, many = True)
        return Response(reply_serializer.data) 

class ComplaintAPI(APIView):
    def post(self, request):

    # Handle product addition
            serializer = ComplaintSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Complaint sent successfully!", "product": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeedbackAPI(APIView):
    def post(self, request):

    # Handle product addition
            serializer = FeedbackSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Feedback sent successfully!", "product": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
    
    


