from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep
from .views import *
from celery import shared_task
from Student_API.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import json


sleeplogger = get_task_logger(__name__)

@shared_task(name='my_first_task')
def my_first_task(duration,report,email):
    message = 'Subject   Marks   Max_Marks\r\r\n'
    for record in report:
        print(record)
        message = message +'   '+ record['subject']+'     ' + str(record['marks']) + str(record['max_marks'])+'\r\r\n'
    print(message)
    subject= 'Student Report'
    message= message
    receiver= email
    is_task_completed= False
    error=''
    print("in celery task")
    try:
        sleep(duration)
        is_task_completed= True
    except Exception as err:
        error= str(err)
        logger.error(error)
    if is_task_completed:
        send_mail(subject,message,EMAIL_HOST_USER,[receiver],fail_silently= False)
        # send_mail_to(subject,message,receivers)
    else:
        send_mail(subject,error,EMAIL_HOST_USER,[receiver],fail_silently= False)
        # send_mail_to(subject,error,receivers)
    print("mailed first_task")
    return('first_task_done')