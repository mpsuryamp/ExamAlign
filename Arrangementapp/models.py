from os import name

from django.db import models



# Create your models here.
class Login(models.Model):
    Username=models.CharField(max_length=100,null=True,blank=True)
    Password=models.CharField(max_length=100,null=True,blank=True)
    Usertype=models.CharField(max_length=100,null=True,blank=True)
    first_name=models.CharField(max_length=100,null=True,blank=True)

class Classroom(models.Model):
    hallno=models.CharField(max_length=20,null=True,blank=True)
    capacity=models.IntegerField(null=True,blank=True)
    columns=models.IntegerField(null=True,blank=True)
    rows=models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(max_length=20, null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(max_length=20, null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
class Semester(models.Model):
    User_id=models.ForeignKey(Login,on_delete=models.CASCADE,null=True,blank=True)
    semestername=models.CharField(max_length=100,null=True,blank=True)

    
class Branch(models.Model):
    branchname=models.CharField(max_length=100,null=True,blank=True)

class Subject(models.Model):
    branch=models.ForeignKey(Branch,on_delete=models.CASCADE,null=True,blank=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True,blank=True)
    subjectname=models.CharField(max_length=100,null=True,blank=True)
    subjectcode=models.CharField(max_length=100,null=True,blank=True)

class ExamDetails(models.Model):
    exam_name = models.CharField(max_length=100, null=True, blank=True)
    exam_subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    exam_date = models.DateField(null=True, blank=True)
    exam_time = models.TimeField(null=True, blank=True)
    no_of_students = models.CharField(max_length=100,null=True,blank=True)
    duration_hours = models.PositiveSmallIntegerField(default=1)  # Duration of the exam in hours
    # Add any other fields related to the exam details
    is_active = models.BooleanField(max_length=20, null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)




class Seating_Arrangement(models.Model):
    classroom_number=models.ForeignKey(Classroom,on_delete=models.CASCADE,null=True,blank=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    exam_date=models.DateField(max_length=100,null=True,blank=True)
    exam_name=models.CharField(max_length=100,null=True,blank=True)
    seat_number=models.CharField(max_length=100,null=True,blank=True)
    exam_time=models.TimeField(max_length=100,null=True,blank=True)
    register_no=models.CharField(max_length=100,null=True,blank=True)


class Staff_Profile(models.Model):
    user=models.ForeignKey(Login,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    staff_id=models.CharField(max_length=100,null=True,blank=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    is_active = models.BooleanField(max_length=20, null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)




class Studentprofile(models.Model):
    user = models.OneToOneField(Login, null=True, blank=True, on_delete=models.CASCADE)
    registerno = models.CharField(max_length=30, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True)
    auto_generate_registerno = models.IntegerField( null=True, blank=True)
    is_active = models.BooleanField(max_length=20, null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if it's a new instance
        if not self.id:
            # Find the maximum registration number for the corresponding branchandsemester
            max_registerno = Studentprofile.objects.filter(branch=self.branch,semester=self.semester).aggregate(models.Max('auto_generate_registerno'))['auto_generate_registerno__max']
            # If no registration numbers exist for this branchandsemester, start with 1
            if max_registerno is None:
                max_registerno = 0
            # Increment the maximum registration number
            self.auto_generate_registerno = max_registerno + 1
        super().save(*args, **kwargs)



class Teacherseatingarrangement(models.Model):
    exam = models.ForeignKey(ExamDetails,on_delete=models.CASCADE, null=True, blank=True)
    exam_hall = models.ForeignKey(Classroom,on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Login,on_delete=models.CASCADE,null=True, blank=True)


class ExamNotification(models.Model):
    notification = models.CharField(max_length=100,null=True,blank=True)
    notification_date = models.DateField(auto_now_add=True,null=True,blank=True)
    

class Complaint(models.Model):
      user = models.ForeignKey(Login, null=True, blank=True, on_delete=models.CASCADE)
      complaints=models.CharField(max_length=300, null=True, blank=True)
      Date=models.DateField(auto_now_add=True, max_length=100,null=True,blank=True)
      Reply = models.CharField(max_length=100,null=True,blank=True)

class Malpractice(models.Model):
    user = models.ForeignKey(Login, null=True, blank=True, on_delete=models.CASCADE)
    registerno = models.CharField(max_length=30, null=True, blank=True)
    Description = models.CharField(max_length=30, null=True, blank=True)
    Image = models.FileField(upload_to='Images/', null=True, blank=True)



    


               
    