
from django.urls import path

from Arrangementapp.models import Login
from Arrangementapp.views import LoginPage
from .views import *


urlpatterns = [
path('', LoginPage.as_view(), name="login"),
path('viewsub/', Viewsub.as_view(),name='viewsub'),
path('addsub/', Addsub.as_view()),
path('editsub/<id>',Editsub.as_view()),
path('deletesub/<id>',Deletesub.as_view()),
path('viewexam/',View_exam.as_view()),
path('addexam/', Add_exam.as_view()),
path('deleteexam/<id>', Deleteexam.as_view()),
path('fetch-subjects/', fetch_subjects, name='fetch_subjects'),
path('viewclassroom/', ViewClassroom.as_view(),name='viewclassroom'),
path('addclassroom/', AddClassroom.as_view(), name='addclassroom'),
path('deleteclassroom/<id>',Deleteclassroom.as_view(),name='deleteclassroom'),
path('allocatestaff/',Allocatestaff.as_view(),name='allocatesstaff'),
path('Allocateseat/',Allocateseat.as_view(),name='Allocatesseat'),
path('get_students_count/<str:exam_date>/', get_students_count, name='get_students_count'),
path('get_class_details/<str:classroomId>/', get_class_details, name='get_class_details'),
path('allocateviewstaff/', Allocateviewstaff.as_view(), name='allocateviewstaff'),
path('allocatedeletestaff/<id>', Allocatedeletestaff.as_view(), name='allocatedeletestaff'),
path('viewstaff/', ViewStaff.as_view()),
path('addstaff/', AddStaff.as_view(), name='addclassroom'),
path('deletestaff/<id>', Deletestaff.as_view(), name='deleteclassroom'),


path('UserRegapi',UserRegAPI.as_view(),name='UserReg'),
path('ViewExamHallapi',ViewExamHallAPI.as_view(),name='ViewExamHall'),
path('ViewExamScheduleapi',ViewExamScheduleAPI.as_view(),name='ViewExamSchedule'),
path('ViewExamNotificationapi',ViewExamNotificationAPI.as_view(),name='ViewExamNotification'),
path('ViewReplyapi',ViewReplyAPI.as_view(),name='ViewReply'),
path('Complaintapi',ComplaintAPI.as_view(),name='Complaint'),
path('LoginPageapi',LoginPageAPI.as_view(),name='LoginPage'),
path('Feedbackapi',FeedbackAPI.as_view(),name='Feedback'),


]
