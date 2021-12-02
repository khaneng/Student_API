from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
	first_name = models.CharField(max_length = 200)
	last_name = models.CharField(max_length = 200)
	email = models.CharField(max_length = 200)
	school = models.CharField(max_length = 200)
	
	def __str__(self):
		return self.first_name+" "+self.last_name


class Subject(models.Model):
	name = models.CharField(max_length = 200)
	
	def __str__(self):
		return self.name

class Marks(models.Model):
	student = models.ForeignKey(Student,related_name = 'student')
	subject = models.ForeignKey(Subject,related_name = 'subject')
	marks = models.FloatField(default = 0.0)
	max_marks = models.FloatField(default = 100.0)
	
	def __str__(self):
		return self.student.first_name+" "+self.student.last_name+": "+self.subject.name