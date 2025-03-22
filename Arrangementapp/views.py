from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse

from .models import Login
from Arrangementapp.serializer import *
from .forms import *
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

def assign_seating(classrooms, subjects, students_per_subject, columns_per_class, seats_per_classroom):
    # Initialize the seating arrangement for each classroom
    classroom_seating = []

    # Keep track of the last subject index
    last_subject_index = 0

    # Iterate over each classroom
    for class_index in range(classrooms):
        if columns_per_class[class_index] == 0:
            print(
                f"Error: Number of columns for classroom {class_index + 1} cannot be zero. Skipping this classroom.")
            continue  # Move to the next classroom

        seats_left = seats_per_classroom[class_index]
        seating = []

        # Assign subjects to seats
        for _ in range(seats_per_classroom[class_index]):
            # Find the subject code corresponding to the student index
            remaining_subjects = [subject for subject, num_students in students_per_subject.items() if
                                  num_students > 0]

            # Check if there are remaining subjects with students
            if not remaining_subjects:
                break  # No subjects left with students, exit the loop

            # Calculate modulo index only if remaining_subjects is not empty
            if remaining_subjects:
                next_subject = remaining_subjects[last_subject_index % len(remaining_subjects)]

            # Check if the subject has remaining students
            if students_per_subject[next_subject] == 0:
                print(f"Error: No students left for subject {next_subject}.")
                return None
            

            # Update the remaining students for the selected subject
            students_per_subject[next_subject] -= 1

            # Assign the subject to the seat
            seating.append(f'{next_subject} ({students_per_subject[next_subject] + 1})')

            # Increment the last subject index
            last_subject_index += 1

        # Fill the remaining seats with the 'None' subject between other subjects
        while len(seating) < seats_per_classroom[class_index]:
            remaining_subjects = [subject for subject, num_students in students_per_subject.items() if
                                  num_students > 0]
            # Check if remaining_subjects is empty before performing modulo operation
            if remaining_subjects:
                next_subject = remaining_subjects[last_subject_index % len(remaining_subjects)]
                seating.append(f'Subject None ({seats_left})')
                seats_left -= 1
                last_subject_index += 1
            else:
                break  # No subjects left with students, exit the loop

        classroom_seating.append(seating)

    return classroom_seating
def update_seating_arrangement_register_numbers():
    # Iterate over Seatingarrangement instance
    seating_entries = Seating_Arrangement.objects.all()

    # Iterate over seating entries
    for index, seating_entry in enumerate(seating_entries):
        # Get the subject associated with the seating entry
        subject = seating_entry.subject

        # Get the students associated with the subject, semester, and branch
        students = Studentprofile.objects.filter(semester=subject.semester, branch=subject.branch)

        # Get the register numbers of the students
        register_numbers = [student.registerno for student in students if student.registerno is not None]
        print(register_numbers)

        # Check if there are register numbers available
        if register_numbers:
            print(register_numbers) 
            # Calculate the index to access register numbers cyclically
            i = (index - 1) % len(register_numbers)  # Adjusted indexing to start from zero
            # Update the register number for the current seating entry
            seating_entry.register_no = register_numbers[i]
            seating_entry.save()

class Allocateseat(View):
    def get(self, request):
        classroom_instances = Classroom.objects.all()
        return render(request, 'newallocation1.html', {'classroom_instances': classroom_instances})

    def post(self, request):

        exam_date = request.POST['exam_date']
        print("exam_date",exam_date)
        Seating_Arrangement.objects.filter(exam_date=exam_date).delete()
        classrooms = request.POST.getlist('class_name')
        print("classrooms",classrooms)
        non_null_classrooms = list(filter(lambda x: x is not None, classrooms))
        exam_details = ExamDetails.objects.filter(exam_date=exam_date).all()
        print("exam_details",exam_details)

        # Initialize the dictionary to store students per subject
        students_per_subject = {}
        subject_ids = []
        for exam_detail in exam_details:
            subject_code = exam_detail.exam_subject.subjectcode
            print("subject_code",subject_code)
            subject_id = exam_detail.exam_subject.id
            print("subject_id",subject_id)
            subject_ids.append(subject_id)
            num_students = int(exam_detail.no_of_students)  # Convert to integer
            students_per_subject[subject_code] = num_students
        print("students_per_subject",students_per_subject)
        seats_per_classroom = []
        columns_per_classroom = []
        total_capacity = 0
        total_classroom = 0
        for class_name in classrooms:
            try:
                classroom = Classroom.objects.get(id=class_name)
                capacity = classroom.capacity
                columns = classroom.columns
                seats_per_classroom.append(capacity)
                columns_per_classroom.append(columns)
                total_capacity += capacity
                total_classroom += 1
            except Classroom.DoesNotExist:
                print(f"Classroom with hallno {class_name} does not exist.")
        print("seats_per_classroom",seats_per_classroom)
        print("columns_per_classroom",columns_per_classroom)
        # Call the function to assign seating
        classroom_seating = assign_seating(
            total_classroom, len(exam_details), students_per_subject, columns_per_classroom, seats_per_classroom
        )

        # Now we will assign students to the seating arrangement
        student_list = Studentprofile.objects.filter(branch__in=[exam_detail.exam_subject.branch for exam_detail in exam_details])

        # Iterating over seating arrangements and assigning register numbers
        for i, seating in enumerate(classroom_seating):
            print("i",i,"seating",seating)
            classroom_number = i + 1  # Classroom numbers start from 1
            for seat, subject in enumerate(seating):
                print("seat",seat,"subject",subject)
                try:
                    # Extract subject code and match it with students
                    subject_instance = Subject.objects.filter(subjectcode=subject.split()[0]).first()
                    print("subject_instance",subject_instance)
                    
                    classroom = Classroom.objects.get(id=classrooms[i])
                    print("classroom",classroom)
                    filtered_students = student_list.filter(
                        branch=subject_instance.branch,
                        semester=subject_instance.semester
                    )
                                # Find a student who hasn't been assigned yet
                    student = filtered_students.first()
                    print("student", student)
                    print("subject_instance",subject_code)
                    # print("exam_name",exam_name)
                    if student:
                        # Create a new SeatingArrangement object with the student's register number
                        seating_entry = Seating_Arrangement(
                            classroom_number=classroom, seat_number=seat + 1,
                            subject=subject_instance, exam_date=exam_date,
                            exam_name=exam_details.filter(exam_subject__subjectcode=subject_instance.subjectcode).first().exam_name,
                            exam_time=exam_details.filter(exam_subject__subjectcode=subject_instance.subjectcode).first().exam_time,
                            register_no=student.registerno  # Assign the register number here
                        )
                        exam_name=exam_details.filter(exam_subject__subjectcode=subject_code).first().exam_name
                        print("exam_name",exam_name)

                        print("seating_entry",seating_entry)
                        seating_entry.save()
                        student_list = student_list.exclude(id=student.id)  # Remove assigned student
                except Classroom.DoesNotExist:
                    pass
                except Subject.DoesNotExist:
                    pass

        # After seating arrangement is complete, redirect to the dashboard
        return redirect('/seating_arrangement_view/')    

from django.db.models import Sum
@csrf_exempt
def get_students_count(request, exam_date):
    try:
        print(exam_date)
        # Assuming YourModel has a field 'exam_date' which stores the date of the exam
        students_count = ExamDetails.objects.filter(exam_date=exam_date).aggregate(total_students=Sum('no_of_students')).get('total_students', 0)
        print(students_count)
        return JsonResponse({'students_count': students_count})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@csrf_exempt
def get_class_details(request, classroomId):
    try:
        print(classroomId)
        # Assuming YourModel has a field 'exam_date' which stores the date of the exam
        class_details = Classroom.objects.filter(id=classroomId).first()
        print(class_details)
        response_data = [{'capacity': class_details.capacity, 'columns': class_details.columns}]
        print("rrrrrrrrrrrr",response_data)
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



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
        data={}
        data=request.data
        data['Usertype']='student'
        data['Username']=request.data.get('username')
        data['Password']=request.data.get('password')
        data['first_name']=request.data.get('username')
        data['registerno']=request.data.get('regNo')
        user_serial = UserSerializer(data=data)
        Login_serial = Loginserializer(data=data)
        data_valid = user_serial.is_valid()
        Login_valid = Login_serial.is_valid()

        if data_valid and Login_valid:
            login_profile = Login_serial.save()
            user_serial.save(user=login_profile)
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
        print(username)
        print(password)

        # Validate input
        if not username or not password:
            response_dict["message"] = "failed"
            return Response(response_dict, status=HTTP_400_BAD_REQUEST)

        # Fetch the user from LoginTable
        t_user = Login.objects.filter(Username=username,Password=password).first()
        print(t_user)

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
    def get(self,request,id):
        st_reg=Studentprofile.objects.filter(user__id=id).first()
        print(st_reg)
        examinationhall  = Seating_Arrangement.objects.filter(register_no=st_reg.registerno).all()
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
            complaint = request.data.get('complaint')
            user_lid = request.data.get('user_lid')
            obj = Complaint()
            obj.complaints = complaint
            obj.Reply="pending"
            obj.user = Login.objects.get(id=user_lid)
            obj.save()
            return Response(
                    {"message": "Complaint sent successfully!"},
                    status=status.HTTP_201_CREATED
                )

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
    
class MalpracticeAPI(APIView):
    def post(self, request):

    # Handle product addition
            serializer = MalpracticeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Report sent successfully!", "product": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

            
    
class Malpracticeview(View):
    def get(self,request):
        Malpractice_instances=Malpractice.objects.all()
        print(Malpractice_instances)
        return render(request, 'Malpractice.html', {'Malpractice_instances': Malpractice_instances})
    

def seating_arrangement_view(request):
    classrooms = Classroom.objects.all()
    arrangements = Seating_Arrangement.objects.all()

    context = {
        'classrooms': classrooms,
        'arrangements': arrangements,
    }
    return render(request, 'seating_arrangement.html', context)

class Viewnotification(View):
    def get(self,request):
        noti=ExamNotification.objects.all()
        print(noti)
        return render(request,'viewnotification.html',{'noti':noti})

class Addnotification(View):
    def get(self,request):
        return render(request,'addnotification.html')
    def post(self,request):
        form=Addnotificationform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Viewnotification')
class Editnotification(View):
    def get(self,request,id):
            noti=ExamNotification.objects.get(id=id)
            return render(request,'editnotification.html',{'noti':noti})
    def post(self,request,id):
        noti=ExamNotification.objects.get(id=id)
        form=Addnotificationform(request.POST,instance=noti)
        if form.is_valid():
            form.save()
            return redirect('')
class Deletenotification(View):
    def get(self,request,id):
        noti=ExamNotification.objects.get(id=id)
        noti.delete()
        return redirect('Viewnotification')
class TeacherseatingAPI(APIView):
    def get(self,request,id):
        teacherseating  = Teacherseatingarrangement.objects.filter(teacher__id=id).all()
        teacherseating_serializer = Teacherseatingarrangementserializer(teacherseating, many = True)
        return Response(teacherseating_serializer.data)
    
class ViewFeedback(View):
    def get(self, request):
        # Render the form template
        staff_instances=Complaint.objects.all()
        return render(request, 'viewfeedback.html',{'staff_instances':staff_instances})

def get_exam_halls(request):
    exam_date = request.GET.get('exam_date')
    print(exam_date)
    from datetime import datetime

    # Input date string
    date_string = "April 27, 2024"

    # Parse the input date string into a datetime object
    date_object = datetime.strptime(date_string, "%B %d, %Y")

    # Convert the datetime object to the desired format
    formatted_date = date_object.strftime("%Y-%m-%d")

    print(formatted_date)
    exam_halls = Classroom.objects.filter(seating_arrangement__exam_date=formatted_date).values('hallno').distinct()
    print(exam_halls)
    return JsonResponse(list(exam_halls), safe=False)


class SemesterList(APIView):
    def get(self, request):
        response={}
        semesters = Semester.objects.all()
        serializer = SemesterSerializer(semesters, many=True)
        branches = Branch.objects.all()
        serializer1 = BranchSerializer(branches, many=True)
        response['semesters'] = serializer.data
        response['branches'] = serializer1.data
        return Response(response)

