
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studentprofile
        fields = ['registerno','branch','semester']

class Loginserializer(serializers.ModelSerializer):
    class Meta:
        model=Login
        fields=['Username','Password','Usertype','first_name']



class ExaminationHallserializer(serializers.ModelSerializer):
    class Meta:
        model = Seating_Arrangement
        fields = [
            'classroom_number', 'subject', 'exam_date',
            'exam_name', 'seat_number','exam_time','register_no']
        
class ExamScheduleserializer(serializers.ModelSerializer):
    class Meta:
        model = ExamDetails
        fields = [
            'no_of_students', 'exam_subject', 'exam_date',
            'exam_name', 'duration_hours','exam_time',]  

class ExamNotificationserializer(serializers.ModelSerializer):
    class Meta:
        model = ExamNotification
        fields = [
            'notification','notification_date','user_type'] 

class Replyserializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['User', 'Reply', 'Date']        
        
class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['complaints', 'Reply']     

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['user','complaints', 'Reply', 'Date']  


class MalpracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Malpractice
        fields = ['user','registerno', 'Description', 'Image']  


class Teacherseatingarrangementserializer(serializers.ModelSerializer):
    # classroom_details = ExaminationHallserializer(source='exam_hall', read_only=True)

    # exam_details = ExamScheduleserializer(source='exam', read_only=True)
    class Meta:
        model = Teacherseatingarrangement
        fields = ['id', 'exam_hall', 'exam']

    def to_representation(self, instance):
    # Get the original representation (default serialization)
        representation = super().to_representation(instance)
        
        # Access the related ExamDetails object
        exam_details = instance.exam  # This is the related ExamDetails object

        # Add exam name and exam time directly to the top-level response
        if exam_details:
            representation['exam_name'] = exam_details.exam_name
            representation['exam_time'] = exam_details.exam_time
            representation['exam_date'] = exam_details.exam_date
        
        return representation

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'User_id', 'semestername']

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'branchname']