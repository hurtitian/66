from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from homepage.models import *

import random

import json

# Create your views here.

def AUTH(func):
    def replace(request, *arg, **kwargs):
        try:
            nameid = request.COOKIES['nameid']
            islogin = request.COOKIES['islogin']
        except Exception as e:
            print(e)
            return render(request, 'homepage/register-fail.html')

        try:
            res = UserInfo.objects.get(id=nameid)
            if res != None:
                return func(request, *arg, **kwargs)
        except Exception as e:
            print(e)
            return render(request, 'homepage/register-fail.html')

    return replace


def record(request):
    # 'nickname': ['222222'], 'email': ['2936435008@qq.com'], 'passwd': ['222222', '222222']
    try:
        user = UserInfo()
        user.nickname = request.POST['nickname']
        user.emailaddr = request.POST['email']
        user.passwd = request.POST['passwd']

        user.save()

        res = redirect('/index')
        res.set_cookie('nameid', user.id, max_age=60 * 60 * 24 * 7 )
        res.set_cookie('islogin', 1, max_age=60 * 60 * 24 * 7 )
        res.set_cookie('name', user.nickname, max_age=60 * 60 * 24 * 7)

        return res
    except:
        return render(request, 'homepage/register-fail.html')


def index(request):
    return render(request, 'homepage/index.html')


@AUTH
def user(request):
    nameid = request.COOKIES['nameid']
    islogin = request.COOKIES['islogin']

    res = UserInfo.objects.get(id=nameid)
    try :
        res.addr = res.useraddr_set.get().addr
    except:
        res.addr = ''
    return render(request, 'homepage/user.html', context={'user': res})


def register(request):
    return render(request, 'homepage/register.html')

@AUTH
def set_recv_addr(request):
    try:
        try:
            address = UserAddr.objects.get(user_id=request.COOKIES['nameid'])
            if address != None:
                address.addr = request.POST['addr']
                address.save()
        except Exception as e:
            print(e)
            addr = UserAddr()
            addr.user_id = UserInfo.objects.get(id=request.COOKIES['nameid'])
            addr.addr = request.POST['addr']
            addr.save()
        return JsonResponse({'code': 1})

    except Exception as e:
        print(e)
        return JsonResponse({'code': 0})

@AUTH
def user_exit(request):
    res = redirect('/index')
    res.delete_cookie('nameid')
    res.delete_cookie('islogin')
    res.delete_cookie('name')

    return res


@AUTH
def unregister(request):

    nameid = request.COOKIES['nameid']
    islogin = request.COOKIES['islogin']

    res = UserInfo.objects.get(id=nameid)

    res.delete()

    res = redirect('/index')
    res.delete_cookie('nameid')
    res.delete_cookie('islogin')
    res.delete_cookie('name')


    return res


def login(request):


    return render(request,'homepage/login.html')



def landing(request):
    # 'nickname': ['222222'], 'email': ['2936435008@qq.com'], 'passwd': ['222222', '222222']

    nickname = request.POST['nickname']
    passwd = request.POST['passwd']

    try:
        user = UserInfo.objects.get(nickname=nickname)
        if user.passwd == passwd:
            res = redirect('/index')
            res.set_cookie('nameid', user.id, max_age=60 * 60 * 24 * 7)
            res.set_cookie('islogin', 1, max_age=60 * 60 * 24 * 7)
            res.set_cookie('name', user.nickname, max_age=60 * 60 * 24 * 7)

            return res
        else:
            return render(request, 'homepage/login-fail.html')
    except:
        return render(request,'homepage/login-fail.html')


@AUTH
def changepasswd(request):

    return render(request,'homepage/change-passwd.html')

@AUTH
def changepasswd_ed(request):

    # 'nickname': ['111111'], 'email': ['2936435008@qq.com'], 'passwd': ['222222'], 'passwdconfirm': ['222222']
    user = UserInfo.objects.get(nickname=request.POST['nickname'])

    user.passwd = request.POST['passwd']
    user.emailaddr = request.POST['email']

    user.save()

    return redirect('/user')


def probe(request):
    try:
        name = request.POST['name']
    except:
        name = None
    if name == None:
        return JsonResponse({'code':0})

    isexie = True
    try:
        user = UserInfo.objects.get(nickname=name)
        if user != None:

            return JsonResponse({'code': 1})
    except:
        return JsonResponse({'code':0})



@AUTH
def comment(request):

    try:
        comments = Comment.objects.all()
        for comment in comments :

            comment.nickname = comment.user_id.nickname


        return render(request,'homepage/comment.html',context={'comments':list(comments)})
    except Exception as e:
        print(e)
        return render(request, 'homepage/comment.html', context={'comments': list(comments)})

@AUTH
def detail(request,bookid):

    if bookid == '':
        bookid = 0
    book = BookInfo.objects.get(id=bookid)

    return render(request,'homepage/detail.html',context={'book':book})

@AUTH
def order(request,bookid):

    book = BookInfo.objects.get(id=bookid)

    return render(request,'homepage/order.html',context={'book':book})


def get_express_no():
    temp = [random.randint(0, 9) for i in range(10)]
    mmp = ''
    for it in temp:
        mmp += str(it)

    return mmp

@AUTH
def confirm_order(request):
    # create oreder
    try:
        bookid = request.POST['bookid']
        order = Order()
        book = BookInfo.objects.get(id=bookid)
        if book.stock <= 0:
            return JsonResponse({'code': 0})
        else:
            book.stock -= 1
            book.save()
        order.book_id = book
        order.book_price = BookInfo.objects.get(id=bookid).price
        order.user_id = UserInfo.objects.get(id=request.COOKIES['nameid'])
        order.recv_addr = UserInfo.objects.get(id=request.COOKIES['nameid']).useraddr_set.get()
        temp = get_express_no()
        order.express_no = temp

        order.save()
        return JsonResponse({'code': 1})
    except Exception as e:
        print(e)
        return JsonResponse({'code': 0})

    # send email to user



@AUTH
def orders(request):

    # create order
    user = UserInfo.objects.get(id=request.COOKIES['nameid'])
    orders = user.order_set.all()

    context_data = []

    for order in orders:
        temp=dict()
        temp['id'] = order.id
        temp['username'] = order.user_id.nickname
        temp['bookname'] = order.book_id.name
        temp['createdata'] = order.createdata
        temp['book_price'] = order.book_price
        temp['recv_addr'] = order.recv_addr
        temp['express_no'] = order.express_no
        context_data.append(temp)




    # order add attribution

    return render(request,'homepage/orders.html',context={'orders':context_data})

@AUTH
def have_recv_addr(request):

    # create order
    try:
        userid = request.POST['userid']
        user = UserInfo.objects.get(id=userid)
        useraddr = user.useraddr_set.get()
        response_data = dict()
        if useraddr != None:
            response_data['code'] = 1
            response_data['recv_addr'] = str(useraddr)
            return JsonResponse( data=response_data)
        else:
            response_data['code'] = 0
            return JsonResponse(data=response_data)

    except Exception as e:
        response_data = dict()
        print(e)
        response_data['code'] = 0
        return JsonResponse(data=response_data)


    # order add attribution



@AUTH
def add_comment(request):
    try:

        # {'userid': ['jiujue'], 'content': ['i have a dream.']}
        comment = Comment()

        comment.comment = str(request.POST['content'])
        comment.user_id = UserInfo.objects.get(id=request.POST['userid'])

        comment.save()

        return JsonResponse(data={'code': 1})

    except Exception as e:
        print(e)
        return JsonResponse(data={'code': 0})



@AUTH
def search(request):

    try:
        word = request.GET['searchwd']
        print('*'*8,word)
        # exclude(body_text__icontains="food")
        books1 = BookInfo.objects.filter(name__icontains=word)
        books2 = BookInfo.objects.filter(authors__icontains=word)
        books3 = BookInfo.objects.filter(press__icontains=word)
        books4= BookInfo.objects.filter(classify__icontains=word)
        books = []
        if(books1!=None):
            for book in books1:
                if book not in books:
                    books.append(book)
        if(books2!=None):
            for book in books2:
                if book not  in books:
                    books.append(book)
        if(books3!=None):
            for book in books3:
                if book not in books:
                    books.append(book)
        if(books4!=None):
            for book in books4:
                if book not in books:
                    books.append(book)
        print(books)
        print(books1)
        print(books2)
        print(books3)
        print(books4)
        return render(request, 'homepage/search.html', context={'books': books})
    except Exception as e:
        print(e)
        return render(request, 'homepage/search.html',)






@AUTH
def get_zone(request,pid):

    zones = China.objects.filter(pid=pid)
    response_data = []

    for zone in zones:
        temp=dict()
        temp['id'] = zone.id
        temp['name'] = zone.name
        response_data.append(temp)


    if response_data == []:
        return JsonResponse({'code': 0,})

    return JsonResponse({'code':1,'zones': response_data})
@AUTH
def test(request):



    return render(request,'homepage/city-prov-znoe.html')

