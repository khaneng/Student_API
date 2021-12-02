from django.shortcuts import render
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializers import StudentSerializer,SubjectSerializer,MarksSerializer
from .models import Student,Subject,Marks
from student.tasks import my_first_task 
from celery.result import AsyncResult
from django.core.mail import send_mail
from Student_API.settings import EMAIL_HOST_USER
import json
from django.forms.models import model_to_dict
from django.core import serializers



# Create your views here.

class UpdateStudentApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	serializer_class = StudentSerializer
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		student_field = request.data.copy()
		student_field.pop('student_id')
		student = Student.objects.filter(id = request.data.get('student_id'))
		student.update(**student_field)
		serializer = self.get_serializer(student.first())
						
		return Response({
			"student": serializer.data,
		})

class UpdateSubjectApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	serializer_class = SubjectSerializer
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		subject_field = request.data.copy()
		subject_field.pop('subject_id')
		subject = Subject.objects.filter(id = request.data.get('subject_id'))
		subject.update(**subject_field)
		serializer = self.get_serializer(subject.first())
						
		return Response({
			"subject": serializer.data,
		})


class UpdateMarksApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	serializer_class = MarksSerializer
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		field = request.data.copy()
		field.pop('subject_id')
		field.pop('student_id')
		marks = Marks.objects.filter(subject = request.data.get('subject_id'),student = request.data.get('student_id'))
		marks.update(**field)
		serializer = self.get_serializer(marks.first())
						
		return Response({
			"subject": serializer.data,
		})
class StudentApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	serializer_class = StudentSerializer
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		serializer = self.get_serializer(data = request.data)
		serializer.is_valid(raise_exception=True)
		try:
			student = serializer.save()
		except Exception as e:
			raise e
				
		return Response({
			"student": serializer.data,
		})


	def get(self, request, *args,  **kwargs):
		queryset = Student.objects.all()
		serializer = self.get_serializer(queryset, many = True)
						
		return Response({
			"student": serializer.data,
		})


class SubjectApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	serializer_class = SubjectSerializer
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		serializer = self.get_serializer(data = request.data)
		serializer.is_valid(raise_exception=True)
		try:
			subject = serializer.save()
		except Exception as e:
			raise e
				
		return Response({
			"subject": serializer.data,
		})


	def get(self, request, *args,  **kwargs):
		queryset = Subject.objects.all()
		serializer = self.get_serializer(queryset, many = True)
						
		return Response({
			"subject": serializer.data,
		})


class MarksApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	serializer_class = MarksSerializer
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		request.data['student'] = request.data.get('student_id')
		request.data['subject'] = request.data.get('subject_id')
		serializer = self.get_serializer(data = request.data)
		serializer.is_valid(raise_exception=True)
		try:
			marks = serializer.save()
		except Exception as e:
			raise e
				
		return Response({
			"marks": serializer.data,
		})

	def get(self, request, *args,  **kwargs):
		queryset = Marks.objects.filter(student = request.GET.get('student_id'))
		serializer = self.get_serializer(queryset, many = True)
						
		return Response({
			"marks": serializer.data,
		})



class StudentReportApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		print("in report")
		marks = Marks.objects.filter(student = request.data.get('student_id')).select_related('subject')
		email = marks[0].student.email
		report = list()
		
		for m in marks:
			record = dict()
			record['subject'] = m.subject.name
			record['marks'] = m.marks
			record['max_marks'] = m.max_marks
			report.append(record)
		# request.data['subject'] = request.data.get('subject_id')
		task = my_first_task.delay(10,report,email)
		print(task.task_id)
		return Response({
			"job_id": task.task_id,
		})


class JobStatusApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		print("in status")
		res = AsyncResult(request.data.get('job_id'))
		print(res.state)
		
		return Response({
			"status": res.state,
		})


