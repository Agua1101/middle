import random
import string
import time

from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

# Create your views here.
from carapp.car import Cart
from dangdangapp.models import *
from log_regist_app import secret


def index(request):
    book = TBook.objects.all()
    book_v = book.order_by('-sales_volume')
    book_d = book.order_by('-publish_date')
    cate = DCategory.objects.all()
    o_cate = request.GET.get('cate')  # 二级分类
    if o_cate == None:
        o_cate = 1
    s_cate = DCategory.objects.filter(category=o_cate)[0]
    name = request.session.get("judge")
    return render(request,'index.html',{'book':book,'cate':cate,'name':name,'s_cate':s_cate,'book_v':book,'book_d':book_d})

def book_details(request):
    book_id = request.GET.get('book')
    if book_id == None:
        book_id = 1
    book = TBook.objects.filter(id=book_id)[0]
    o_cate = request.GET.get('cate')  # 二级分类
    if o_cate == None:
        o_cate = 16
    s_cate = DCategory.objects.filter(category=o_cate)[0]
    d_id = DCategory.objects.filter(category=o_cate)[0].category_pid   # 一级分类
    if d_id == 0:
        d_id = o_cate
    d_cate = DCategory.objects.filter(category=d_id)[0]
    s_id = DCategory.objects.filter(category_pid=o_cate)
    # ---------------左上角登录--------------
    name = request.session.get("judge")

    return render(request,'Book details.html',{'book':book,'s_cate':s_cate,'d_cate':d_cate,'s_id':s_id,'name':name})

def book_list(request):
    number = request.GET.get('number')
    o_cate = request.GET.get('cate')
    cate = DCategory.objects.all()
    if o_cate == None:
        o_cate = 16
    s_cate = DCategory.objects.filter(category=o_cate)[0]
    d_id = DCategory.objects.filter(category=o_cate)[0].category_pid     #主分类id

    if d_id == 0:
        d_id = o_cate
        # s_cate = DCategory.objects.filter(category=o_cate)[0]
    s_id = DCategory.objects.filter(category_pid=o_cate)         #主分类下所有子分类的id
    d_cate = DCategory.objects.filter(category=d_id)[0]

    #-------------分页----------------

    book_id = s_cate.category
    book = TBook.objects.filter(book_category=book_id)
    if int(o_cate) < 16:
        book_all = DCategory.objects.filter(category_pid= o_cate)
        book_l = []
        for i in book_all:
            book_id = i.category
            book_l.append(book_id)
            book = TBook.objects.filter(book_category__in = book_l)
    if not number:
        number = 1
    pagtor = Paginator(book, per_page=4)
    page = pagtor.page(number)
    #---------------左上角登录--------------
    name = request.session.get("judge")


    return render(request,'booklist.html',{'s_cate':s_cate,'d_cate':d_cate,'cate':cate,'page':page,'s_id':s_id,'name':name,'d_id':d_id})

def kill_session(request):
    del request.session['judge']
    position = request.GET.get('position')
    if position == 'index':
        return redirect('dangdangapp:index')
    elif position == 'booklist':
        return redirect('dangdangapp:book_list')
    elif position == 'bookdetails':
        return redirect('dangdangapp:book_details')
    elif position == 'indent':
        return redirect('carapp:car')


def indent(request):
    name = request.session.get("judge")
    if name:
        user = TUser.objects.filter(t_email=name)[0]
        id = user.id
        address = TAddress.objects.filter(user_id=id)
        cart = request.session.get('cart')
        book_all = cart.cartItem
        to = cart.total_price

        return render(request,'indent.html',{'name':name,'book':book_all,'total':to,'address':address,'user_id':id})

    return redirect('/log_regist/login/?position=indent')


def indent_ok(request):
    try:
        with transaction.atomic():
            id = int(request.GET.get('id'))
            userid = int(request.GET.get('userid'))
            # print(userid)
            order = secret.order_secret()
            ti = time.time()
            ti_local = time.localtime(ti)
            now = time.strftime("%Y-%m-%d %H:%M:%S",ti_local)
            cart = request.session.get('cart')
            book_all = cart.cartItem
            to = cart.total_price

            TOrder.objects.create(num=order,create_time=now,price=to,order_addrid=id,order_uid=userid)
            order_all = TOrder.objects.filter(num=order)[0]
            order_id = order_all.id
            for i in book_all:
                bookid = i.book.id
                amount = int(i.amount)
                DOrderiterm.objects.create(shop_bookid=bookid,shop_ordid=order_id,shop_num=amount,total_price=to)
            return render(request, 'indent ok.html',{'order':order})
    except:
        return HttpResponse('订单提交失败')

def choose(request):
    id = request.POST.get('id')
    if id == 'new':
        return JsonResponse({'result':1,'man':'','det_address':'','zip_code':'','moble':'','tel':''})
    print(id)
    address = TAddress.objects.filter(id=id)[0]
    man = address.name
    det_address = address.detail_address
    zip_code = address.zipcode
    moble = address.addr_mobile
    tel = address.telphone

    return JsonResponse({'result':1,'man':man,'det_address':det_address,'zip_code':zip_code,'moble':moble,'tel':tel})

def present(request):
    man = request.POST.get('man')
    address = request.POST.get('address')
    zipcode = request.POST.get('zipcode')
    moble = request.POST.get('moble')



    if moble:
        int(moble)
    tel = request.POST.get('tel')
    if tel:
        int(tel)
    userid = int(request.POST.get('userid'))
    print(man,address,zipcode,moble,tel,userid)
    address_all = TAddress.objects.filter(user_id=userid)
    if address_all.count() == 0:
        if tel:
            print(1)
            TAddress.objects.create(name=man, detail_address=address, zipcode=zipcode, telphone=tel,user_id=userid, less_address=man)
            order = TAddress.objects.filter(name=man, detail_address=address, zipcode=zipcode, telphone=tel,user_id=userid, less_address=man)[0]
            id = order.id
            return JsonResponse({'result': 1,'id':id,'userid':userid})
        elif moble:
            print(2)
            TAddress.objects.create(name=man, detail_address=address, zipcode=zipcode, addr_mobile=moble, user_id=userid,
                                    less_address=man)
            order = TAddress.objects.filter(name=man, detail_address=address, zipcode=zipcode, telphone=tel, user_id=userid,
                                    less_address=man)[0]
            id = order.id
            return JsonResponse({'result': 1,'id':id,'userid':userid})
    else:
        for i in address_all:
            if not (i.name == man and i.detail_address == address and i.zipcode == zipcode and i.addr_mobile == moble) or (i.name == man and i.detail_address == address and i.zipcode == zipcode and i.telphone == tel):
                if tel:
                    print(3)
                    TAddress.objects.create(name=man, detail_address=address, zipcode=zipcode, telphone=tel,
                                            user_id=userid, less_address=man)
                    order = TAddress.objects.filter(name=man, detail_address=address, zipcode=zipcode, telphone=tel,
                                                    user_id=userid, less_address=man)[0]
                    id = order.id
                    return JsonResponse({'result': 1,'id':id,'userid':userid})
                elif moble:
                    print(4)
                    TAddress.objects.create(name=man, detail_address=address, zipcode=zipcode, addr_mobile=moble,
                                            user_id=userid,
                                            less_address=man)
                    order = TAddress.objects.filter(name=man, detail_address=address, zipcode=zipcode, addr_mobile=moble,
                                                    user_id=userid, less_address=man)[0]
                    print(order)
                    id = order.id
                    print(id)
                    return JsonResponse({'result': 1,'id':id,'userid':userid})
        order = TAddress.objects.filter(name=man, detail_address=address, zipcode=zipcode, telphone=tel, user_id=userid,
                                    less_address=man)[0]
        id = order.id
        return JsonResponse({'result':1,'id':id,'userid':userid})




