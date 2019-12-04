from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
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
        res.set_cookie('nameid', user.id, max_age=60 * 60 * 24 * 7)
        res.set_cookie('islogin', 1, max_age=60 * 60 * 24 * 7)
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
    try:
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


    return render(request, 'homepage/login.html')


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
        return render(request, 'homepage/login-fail.html')


@AUTH
def changepasswd(request):
    return render(request, 'homepage/change-passwd.html')


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
        return JsonResponse({'code': 0})

    isexie = True
    try:
        user = UserInfo.objects.get(nickname=name)
        if user != None:
            return JsonResponse({'code': 1})
    except:
        return JsonResponse({'code': 0})


@AUTH
def comment(request):
    try:
        comments = Comment.objects.all().order_by('-createdata')
        for comment in comments:
            comment.nickname = comment.user_id.nickname

        print('send recommend')
        res = send_recommend(request.COOKIES['nameid'],)
        print('sent recommend',res)

        return render(request, 'homepage/comment.html', context={'comments': list(comments)})
    except Exception as e:
        print(e)
        return render(request, 'homepage/comment.html', context={'comments': list(comments)})


@AUTH
def detail(request, bookid):
    if bookid == '':
        bookid = 0
    book = BookInfo.objects.get(id=bookid)

    return render(request, 'homepage/detail.html', context={'book': book})


@AUTH
def order(request, bookid):
    book = BookInfo.objects.get(id=bookid)

    return render(request, 'homepage/order.html', context={'book': book})


def get_express_no():
    temp = [random.randint(0, 9) for i in range(10)]
    mmp = ''
    for it in temp:
        mmp += str(it)

    return mmp

def reset_recommend(request,books):
    recommend = []
    if books != None:
        for it in books:
            recommend.append(it.classify)

    user = UserInfo.objects.get(id=request.COOKIES['nameid'])
    try:

        user.recommend_set.get().delete()
    except Exception as e:
        if str(e) == 'Recommend matching query does not exist.':

            print('no exist recommend ,but we will save something new stuff.')
            newrecommend = Recommend()
            newrecommend.user_id = user
            newrecommend.word_list = ','.join(recommend)
            newrecommend.save()
            return True

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
            order.book_id = book
            order.book_price = BookInfo.objects.get(id=bookid).price
            order.user_id = UserInfo.objects.get(id=request.COOKIES['nameid'])
            order.recv_addr = UserInfo.objects.get(id=request.COOKIES['nameid']).useraddr_set.get()
            temp = get_express_no()
            order.express_no = temp

            reset_recommend(request,[order.book_id,],)
            book.stock -= 1
    
            order.save()
            book.save()
               
            if 1 == send(order):
                return JsonResponse({'code': 1})
            else:
                del order
                return JsonResponse({'code': 0})
    except Exception as e:
        print(e)
        return JsonResponse({'code': 0})

    # send email to user


@AUTH
def orders(request):
    # create order
    user = UserInfo.objects.get(id=request.COOKIES['nameid'])
    orders = user.order_set.all().order_by('-createdata')

    context_data = []

    for order in orders:
        temp = dict()
        temp['id'] = order.id
        temp['username'] = order.user_id.nickname
        temp['bookname'] = order.book_id.name
        temp['createdata'] = order.createdata
        temp['book_price'] = order.book_price
        temp['recv_addr'] = order.recv_addr
        temp['express_no'] = order.express_no
        context_data.append(temp)

    # order add attribution

    return render(request, 'homepage/orders.html', context={'orders': context_data})


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
            return JsonResponse(data=response_data)
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
        print('*' * 8, word)
        # exclude(body_text__icontains="food")
        books1 = BookInfo.objects.filter(name__icontains=word)
        books2 = BookInfo.objects.filter(authors__icontains=word)
        books3 = BookInfo.objects.filter(press__icontains=word)
        books4 = BookInfo.objects.filter(classify__icontains=word)
        books = []
        if (books1 != None):
            for book in books1:
                if book not in books:
                    books.append(book)
        if (books2 != None):
            for book in books2:
                if book not in books:
                    books.append(book)
        if (books3 != None):
            for book in books3:
                if book not in books:
                    books.append(book)
        if (books4 != None):
            for book in books4:
                if book not in books:
                    books.append(book)

        reset_recommend ,args=(request,books)



        return render(request, 'homepage/search.html', context={'books': books})
    except Exception as e:
        print(e)
        return render(request, 'homepage/search.html', )


@AUTH
def get_zone(request, pid):
    zones = China.objects.filter(pid=pid)
    response_data = []

    for zone in zones:
        temp = dict()
        temp['id'] = zone.id
        temp['name'] = zone.name
        response_data.append(temp)

    if response_data == []:
        return JsonResponse({'code': 0, })

    return JsonResponse({'code': 1, 'zones': response_data})


@AUTH
def test(request):
    return render(request, 'homepage/city-prov-znoe.html')


def send(order):
    return 1
    msg = """<ul style="list-style: none;background-color: #e2e9e7;padding-left: 0;margin: 20px auto;width: 600px;height: 160px">
                <hr style="margin-top: 4px;margin-bottom: 4px"/>
                <li>{book_name}</li>
                <hr style="margin-top: 4px;margin-bottom: 4px"/>
                <li>{book_price}</li>
                <hr  style="margin-top: 4px;margin-bottom: 4px"/>
                <li>{user_name}</li>
                <hr  style="margin-top: 4px;margin-bottom: 4px"/>
                <li>{recv_addr}</li>
                <hr  style="margin-top: 4px;margin-bottom: 4px"/>
                <li>{express_no}</li>
                <hr  style="margin-top: 4px;margin-bottom: 4px"/>
            </ul>"""
    style = """
        <style>
            .con:hover {
                color: greenyellow;
            }
        
            .wrapper {
                width: 340px;
                overflow: hidden;
                height: 540px;
                background-color: rgba(193, 195, 197, 0.8);
                margin: 20px auto
            }
        
            .inner {
                list-style: none;
                background-color: rgba(251, 253, 251, 0.8);
                margin: 20px auto;
                width: 300px;
                border: silver solid 1px;
                padding: 6px;
                height: 480px
            }
            </style>"""
    msg = '''
            <div class="wrapper">
                <ul class="inner">
                    <div class="con">
                        <li style="font-size: 30px;text-align: center;">Bill</li>
                    </div>
                    <hr/>
                    <div class="con">
                        <li>Book Name:</li>
                    </div>
                    <hr/>
                    <div class="con">
                        <li style="text-indent: 20px">{book_name}</li>
                    </div>
                    <hr/>
                    <div class="con">
                        <li>Price:</li>
                    </div>
                    <hr/>
                    <div class="con">
                        <li style="text-indent: 20px">￥ {book_price}</li>
                    </div>
                    <hr/>
                    <div class="con">
                        <li>User Name:</li>
                    </div>
                    <hr/>
                    <div class="con">
                    </div>
                    <li style="text-indent: 20px">{user_name}</li>
                    <hr/>
                    <div class="con">
                        <li>Recv addr:</li>
                    </div>
                    <hr/>
                    <div class="con">
                        <li style="text-indent: 20px">{recv_addr}</li>
                    </div>
                    <hr/>
                    <div class="con">
                        <li>Express On:</li>
                    </div>
                    <hr/>
                    <div class="con">
                        <li style="text-indent: 20px">{express_no}</li>
                    </div>
                    <hr/>
                    <div class="con">
                        <a  style="float: right;background:rgba(223,235,248,0.48);" href='http://{domain}/orders'>Go Orders!</button>
                        <a  style="float: left;background:rgba(223,235,248,0.48);" href='http://{domain}/user'>Go Pay ! !</button>
                    </div>
                </ul>
            </div>
        '''.format(book_name=order.book_id.name,
                   book_price=order.book_price,
                   user_name=order.user_id.nickname,
                   recv_addr=order.recv_addr,
                   express_no=order.express_no,
                   domain=settings.MY_DOMAIN,)

    res = send_mail(subject='StockHub-Order', message='This is an order of your', from_email=settings.EMAIL_FROM,
                    recipient_list=['StockHub-%s<%s>' % (order.user_id.nickname,order.user_id.emailaddr)], html_message=style+msg, fail_silently=False)

    return res


def send_recommend(userid):
    return 1

    user = UserInfo.objects.get(id=userid)
    try:
        word = str(user.recommend_set.get().word_list).split(',')[0]


        book = BookInfo.objects.get(classify__icontains=word)

        msg = '<a href="http://'+settings.MY_DOMAIN+'/"> 你喜欢的{classify}类型书籍更新了，来看看吧</a>' .format(classify=book.classify)

        res = send_mail(subject='StockHub-Recommend', message='This is an order of your',
                        from_email=settings.EMAIL_FROM,
                        recipient_list=['StockHub-%s<%s>' % (user.nickname, user.emailaddr)],
                        html_message=msg, fail_silently=False)
        return res
    except Exception as e:
        if str(e) == 'Recommend matching query does not exist.' or str(e) == 'BookInfo matching query does not exist.':

            print('no would recommend,but we will send a common.')
            msg = '<a href="http://'+settings.MY_DOMAIN+'"> 有你喜欢的类型书籍更新了，来看看吧</a>'

            res = send_mail(subject='StockHub-Recommend', message='This is an order of your', from_email=settings.EMAIL_FROM,
                            recipient_list=['StockHub-%s<%s>' %(str(user.nickname),str(user.emailaddr)),],
                            html_message=msg, fail_silently=False)
            return res
        else:
            print(e)

