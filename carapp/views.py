import time

from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
# Create your views here.
from carapp.car import Cart,CartItem,ReCart
from dangdangapp.models import TBook


def car(request):
    # try:
        name = request.session.get("judge")
        cart = request.session.get('cart')
        re_cart = request.session.get('re_cart')
        if not cart:
            return render(request,'car.html')
        book = cart.cartItem
        n = 0
        for i in book:
            n += i.amount
        if not re_cart:
            save_price = cart.save_price
            total_price = cart.total_price
            return render(request,'car.html',{'book':book,'save_price':save_price,'total_price':total_price,'name':name,'n':n})
        del_book = re_cart.cartItem_del
        # print(book)
        save_price = cart.save_price
        total_price = cart.total_price
        return render(request,'car.html',{'book':book,'save_price':save_price,'total_price':total_price,'del_book':del_book,'name':name,'n':n})
    # except:
        # cart = Cart()
        # name = request.session.get("judge")
        # cart = request.session.get('cart')
        # book = cart.cartItem
        # save_price = cart.save_price
        # total_price = cart.total_price
        # return render(request,'car.html')

def add_book(request):
    time.sleep(1)
    bookid = request.GET.get('bookid')
    amount = int(request.GET.get('amount'))
    cart = request.session.get('cart')
    print(bookid,amount)
    if not cart:
        cart = Cart()
        cart.add_book_toCart(bookid,amount)
        request.session['cart'] = cart
    else:
        cart.add_book_toCart(bookid,amount)
        request.session['cart'] = cart

    return HttpResponse('1')

def change_num(request):
    bookid = request.GET.get('bookid')
    amount = request.GET.get('amount')
    if amount == "0":
        amount = -1
    print(bookid,amount)
    cart = request.session.get('cart')
    cart.add_book_toCart(bookid, amount)
    request.session['cart'] = cart
    book = cart.cartItem
    n = 0
    for i in book:
        n += i.amount
    to = cart.total_price
    sa = cart.save_price
    return JsonResponse({'result':1,'to':to,'sa':sa,'n':n})

def del_num(request):
    bookid = request.GET.get('bookid')
    amount = int(request.GET.get('amount'))
    print(bookid,amount)

    cart = request.session.get('cart')
    cart.delete_book(bookid)
    to = cart.total_price
    sa = cart.save_price

    re_cart = request.session.get('re_cart')
    if not re_cart:
        re_cart = ReCart()
        re_cart.delete_book(bookid,amount)
        request.session['re_cart'] = re_cart
    else:
        re_cart.delete_book(bookid,amount)
        request.session['re_cart'] = re_cart
    # del_book = re_cart.cartItem_del
    # print(del_book)

    book = TBook.objects.filter(id=bookid)[0]
    name = book.book_name
    market = book.market_price
    dang = book.dang_price
    pic = book.pic_path
    sum_book = amount * dang


    return JsonResponse({'result': 1, 'to': to, 'sa': sa,'bookid':bookid,'name':name,'market':market,'dang':dang,'pic':pic,'sum_book':sum_book})

def update_book(request):
    bookid = request.GET.get('bookid')
    amount = int(request.GET.get('amount'))
    cart = request.session.get('cart')
    if amount > 1:
        cart.change_book(bookid, amount)
        request.session['cart'] = cart
    else:
        amount = 1
        cart.change_book(bookid, amount)
        request.session['cart'] = cart

    book = cart.cartItem
    n = 0
    for i in book:
        n += i.amount
    to = cart.total_price
    sa = cart.save_price
    return JsonResponse({'result': 1, 'to': to, 'sa': sa,'n':n})

def recover(request):
    bookid = request.GET.get('bookid')
    amount = int(request.GET.get('amount'))
    print(bookid,amount)
    re_cart = request.session.get('re_cart')
    re_cart.recover_book(bookid)
    request.session['re_cart'] = re_cart
    cart = request.session.get('cart')
    cart.add_book_toCart(bookid,amount)
    request.session['cart'] = cart

    book = TBook.objects.filter(id=bookid)[0]
    name = book.book_name
    market = book.market_price
    dang = book.dang_price
    pic = book.pic_path
    sum_book = amount * dang

    to = cart.total_price
    sa = cart.save_price


    return JsonResponse({'result': 1, 'to': to, 'sa': sa,'bookid':bookid,'name':name,'market':market,'dang':dang,'pic':pic,'sum_book':sum_book})
