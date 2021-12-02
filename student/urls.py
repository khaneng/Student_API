from django.conf.urls import url
from .views import StudentApi, SubjectApi, MarksApi,UpdateStudentApi,UpdateSubjectApi,UpdateMarksApi,StudentReportApi,JobStatusApi

urlpatterns = [

    url(r'^update/student', UpdateStudentApi.as_view()),
    url(r'^update/subject', UpdateSubjectApi.as_view()),
    url(r'^update/marks', UpdateMarksApi.as_view()),
    url(r'^student', StudentApi.as_view()),
    url(r'^subject',SubjectApi.as_view()),
    url(r'^marks',MarksApi.as_view()),
    url(r'^report/student', StudentReportApi.as_view()),
    url(r'^job/status', JobStatusApi.as_view()),
   
]