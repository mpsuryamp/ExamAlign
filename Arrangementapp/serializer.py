
from rest_framework import serializers
from .models import Login,Seating_Arrangement,ExamDetails,ExamNotification,Complaint, Studentprofile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studentprofile
        fields = ['user','registerno','branch','semester','auto_generate_registerno','is_active','created_at','updated_at']

class Loginserializer(serializers.ModelSerializer):
    class Meta:
        model=Login
        fields=['username']



class ExaminationHallserializer(serializers.ModelSerializer):
    class Meta:
        model = Seating_Arrangement
        fields = [
            'classroom_NO', 'Subject', 'Exam_Date',
            'Exam_Name', 'Seat_NO','Exam_time','Reg_NO']
        
class ExamScheduleserializer(serializers.ModelSerializer):
    class Meta:
        model = ExamDetails
        fields = [
            'no_of_students', 'exam_subject', 'Exam_Date',
            'Exam_Name', 'duration_hours','Exam_time',]  

class ExamNotificationserializer(serializers.ModelSerializer):
    class Meta:
        model = ExamNotification
        fields = [
            'Exam_Date','Exam_Name','Exam_time',] 

class Replyserializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = [
            'User', 'Reply', 'Date']        
        
class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = [
            'User', 'Reply', 'Date']        

