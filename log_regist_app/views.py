import os
import random
import re
import string

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
import time
# Create your views here.
from captcha.image import ImageCaptcha
from dangdangapp.models import TUser, TBook, DCategory, TOrder_ok
from log_regist_app import email_send, secret
from django.core.mail import send_mail

def login(request):
    position = request.GET.get('position')
    # print('login:',position)
    # name = request.COOKIES.get("name") #如果有cookies就 获取登录状态
    # pwd = request.COOKIES.get("password")
    # check = TUser.objects.filter(t_email=name, password=pwd)
    # if check:
    #     request.session["judge"] = name
    #     return redirect('dangdangapp:index')
    name = request.session.get('judge')
    user = TUser.objects.filter(t_email=name)[0]
    state = user.status
    if name and state:
        if position == 'index':
            return redirect('dangdangapp:index')
        elif position == 'booklist':

            return redirect('dangdangapp:book_list')
        elif position == 'bookdetails':

            return redirect('dangdangapp:book_list')
        elif position == 'indent':

            return redirect('dangdangapp:indent')

        return redirect('dangdangapp:index')
    return render(request, 'login.html', {'position':position})

def login_logic(request):
    try:
        position = request.GET.get('position')
        print('login_logic:',position)
        book = TBook.objects.all()
        cate = DCategory.objects.all()
        email = request.POST.get('txtUsername')
        pwd = request.POST.get('txtPassword')
        TUser.objects.filter(t_email=email, password=pwd)
        request.session["judge"] = email
        if position == 'index':
            res = redirect('dangdangapp:index')
            res.set_cookie("name", email)
            res.set_cookie("password", pwd)
            return res
        elif position == 'booklist':
            res = redirect('dangdangapp:book_list')
            res.set_cookie("name", email)
            res.set_cookie("password", pwd)
            return res
        elif position == 'bookdetails':
            res = redirect('dangdangapp:book_details')
            res.set_cookie("name", email)
            res.set_cookie("password", pwd)
            return res
        elif position == 'indent':
            res = redirect('dangdangapp:indent')
            res.set_cookie("name", email)
            res.set_cookie("password", pwd)
            return res
        # res = render(request,'index.html',{'book':book,'cate':cate,'name':email})
        # res.set_cookie("name", email)
        # res.set_cookie("password", pwd)
        # return res
        # return redirect('userapp:emplist')
    except:
        return redirect('userapp:login')


def register(request):
    position = request.GET.get('position')

    return render(request,'register.html',{'position':position})

def register_logic(request):
    try:
        # name = request.POST.get('txt_username')
        # position = request.POST.get('position')
        pwd = request.POST.get('txt_password')
        repwd = request.POST.get('repwd')
        email = request.POST.get('txt_username')
        captcha = request.POST.get('txt_vcode') #获取输入的验证码
        code = request.session.get('code') #获取生成的验证码

        match = re.search('(^\w*@\w*\.\w*)|(^1{1}\d{10}$)', email)
        match_pwd = re.match('\w{8}', pwd)
        if not match:
            return JsonResponse({'check_false':3})
        elif not match_pwd:
            return JsonResponse({'check_false': 4})
        elif not pwd == repwd:
            return JsonResponse({'check_false': 5})
        elif captcha.upper() != code.upper():
            return JsonResponse({'check_false': 2})
        else:
            print('1')
            TUser.objects.create(t_email=email, password=pwd)
            user = TUser.objects.filter(t_email=email)
            id = user[0].id
            order_code = secret.order_secret()
            print(id)
            TOrder_ok.objects.create(t_code=order_code, t_userid=id)

            print(order_code)

            email_send.send_success(order_code,email)

            return JsonResponse({'result': 1, 'email': email})
    except:
        return redirect('log_regist_app:register')

def register_ok(request):
    position = request.GET.get('position')
    email = request.GET.get('email')
    return render(request,'register ok.html',{'position':position,'email':email})

def return_where(request):
    position = request.GET.get('position')
    if position == 'index':
        return redirect('dangdangapp:index')
    elif position == 'booklist':

        return redirect('dangdangapp:book_list')
    elif position == 'bookdetails':

        return redirect('dangdangapp:book_list')
    elif position == 'indent':

        return redirect('dangdangapp:indent')
    return redirect('dangdangapp:index')


def sendEmail_check(request):
    receive = request.GET.get('code')
    check = TOrder_ok.objects.filter(t_code=receive)
    if check:
        id = check[0].t_userid
        user = TUser.objects.filter(id=id)
        uuu = user[0]
        uuu.status = 1
        uuu.save()
        print(1)
        email = user[0].t_email
        request.session["judge"] = email
        return HttpResponse('注册成功')
    return HttpResponse('注册失败')



def getcaptcha(request):
    image = ImageCaptcha(fonts=[os.path.abspath('captcha/data/DroidSansMono.ttf')])
    code = random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits,4)
    random_code = ''.join(code)
    request.session['code'] = random_code
    data = image.generate(random_code)
    return HttpResponse(data,"image/png")

def check_username(request):
    time.sleep(1)
    name = request.GET.get('name')
    # print(name)
    match = re.search('(^\w*@\w*\.\w*)|(^1{1}\d{10}$)',name)
    use_name = TUser.objects.filter(t_name=name)
    if not name:
        return HttpResponse('null')
    elif use_name:
        return HttpResponse('wrong')
    elif not match:
        return HttpResponse('wrong')
    return HttpResponse('right')

def checkpwd(request):
    time.sleep(1)
    pwd = request.POST.get('pwd')
    re_pwd = request.POST.get('re_pwd')
    match = re.match('\w{8}', pwd)
    if not pwd:
        return HttpResponse('null')
    elif not match:
        return HttpResponse('No')
    return HttpResponse('ok')

def checkrepwd(request):
    time.sleep(1)
    pwd = request.POST.get('pwd')
    re_pwd = request.POST.get('re_pwd')
    match = re.match('\w{8}', pwd)
    if not re_pwd:
        return HttpResponse('null')
    elif not match:
        return HttpResponse('No')
    elif pwd == re_pwd:
        return HttpResponse('ok')
    return HttpResponse('No')

def log_name(request):
    time.sleep(1)
    name = request.GET.get('name')
    # print(name)
    match = re.search('(^\w*@\w*\.\w*)|(^1{1}\d{10}$)', name)
    use_name = TUser.objects.filter(t_email=name)
    if not name:
        return HttpResponse('null')
    elif not match:
        return HttpResponse('wrong')
    elif not use_name:
        return HttpResponse('wrong')
    return HttpResponse('right')

def log_pwd(request):
    time.sleep(1)
    pwd = request.POST.get('pwd')
    name = request.POST.get('name')
    print(name)
    user =TUser.objects.filter(t_email=name)[0]
    print(user)
    match = re.match('\w{8}', pwd)
    if not pwd:
        return HttpResponse('null')
    elif not user.password == pwd:
        return HttpResponse('No')
    return HttpResponse('ok')

