from django.conf import settings
from django.core.mail import send_mail

from celery_tasks.main import celery_app
@celery_app.task(name='send_email')
def send_verify_email(verify_url,to_email):
    return send_mail(subject = "美多商城激活邮件",
              message = '',
              from_email = settings.EMAIL_FROM,
              recipient_list = [to_email],
              html_message='<a href="http://www.meiduo.site:8080">激活链接</a>'

              )

