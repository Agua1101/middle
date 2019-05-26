import os
from django.core.mail import send_mail,EmailMultiAlternatives

from middle import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'middle.settings'

def send_success(code,email):
    # print('邮件')
    subject = '测试邮件'
    # from_email = 'agua1101@sina.com'
    # subject, from_email, to = '测试邮件', 'agua1101@sina.com', 'agua1101@sina.com'
    text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你极其幸运'
    # html_content = '<p>感谢注册<a href="http://127.0.0.1:8000/log_regist/sendEmail_check/?code='+code+'target = blank > www.baidu.com < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '
    html_content = '<p>感谢注册<a href="http://{}/?code={}"target = blank > www.baidu.com < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '.format('127.0.0.1:8000/log_regist/sendEmail_check',code)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
