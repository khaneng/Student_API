from django.contrib import admin
from .models import Subject,Student,Marks

# Register your models here.
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Marks)