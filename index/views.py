from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import json

from .forms import *
from .models import *

# Create your views here.
def index_views(request):
    return render(request, 'index.html', locals())

# /login 对应的视图
def login_views(request):
    url = '/'
    if request.method == 'GET':
        # get 的流程
        # 判断session中是否有登录信息
        if 'uid' in request.session and 'uphone' in request.session:
            # session中有值
            return redirect(url)
        else:
            # session中没有值
            # 判断cookie中是否有uid和uphone
            if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
                # cookie中有登录信息
                # 从cookie中取出数据保存进session
                uid = request.COOKIES['uid']
                uphone = request.COOKIES['uphone']
                request.session['uid'] = uid
                request.session['uphone'] = uphone
                # 再重定向到首页或原路径
                return redirect(url)
            else:
                # cookie中没有登录信息
                # 去往登录页面
                form = LoginForm()
                return render(request, 'login.html', locals())
    else:
        # post 的流程
        # 实现登录操作: 取出uphone 和 upwd到db中判断
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        uList = Users.objects.filter(uphone=uphone,upwd=upwd)
        if uList:
            # 登录成功
            # 取出 uphone 和 uid 保存进session
            uid = uList[0].id
            request.session['uphone'] = uphone
            request.session['uid'] = uid
            # 判断是否有记住密码
            resp = redirect(url)
            if 'isSaved' in request.POST:
                # 记住密码的话将值保存进cookie
                expires = 60 * 60 * 24 * 266
                resp.set_cookie('uid', uid, expires)
                resp.set_cookie('uphone', uphone, expires)
            # 重定向到首页或原路径
            return resp
        else:
            # 登录失败
            form = LoginForm()
            errMsg = "用户名或密码不正确"
            return render(request, 'login.html', locals())

# /register 对应的视图
def register_views(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # 实现注册的功能
        dic = {
            'uphone': request.POST['uphone'],
            'upwd': request.POST['upwd'],
            'uemail': request.POST['uemail'],
            'uname': request.POST['uname']
        }
        # 将数据插入进数据库 - 注册
        Users(**dic).save()
        # 根据uphone的值再查询数据库
        u = Users.objects.get(uphone=request.POST['uphone'])
        # 将用户 id 和 Uphone 保存进session
        request.session['uid'] = u.id
        request.session['uphone'] = u.uphone

        return redirect('/')

# 检查手机号码是否存在 -> /check_uphone/
def check_uphone_views(request):
    if request.method == 'POST':
        # 接收前端传递过来的手机号码
        uphone = request.POST['uphone']
        uList = Users.objects.filter(uphone=uphone)
        if uList:
            # 如果条件为真,表示手机号码已经存在
            # 响应 status 值为0, 用于通知客户端手机号码已存在
            # 响应 text 值为 '手机号码已存在'
            dic = {
                "status": "0",
                "text": "手机号码已存在",
            }
            return HttpResponse(json.dumps(dic))
        else:
            dic = {
                "status": "1",
                "text": "可以注册",
            }
            return HttpResponse(json.dumps(dic))

# 检查用户是否登录, 如果有的话则取出uname的值
def check_login_views(request):
    # 判断 session 中是否有uid 和 uphone
    if 'uid' in request.session and 'uphone' in request.session:
        # 用户处于登录状态
        # 根据uid 获取uname 的值
        uid = request.session['uid']
        user = Users.objects.get(id=uid)
        # 根据uid查询对应的user信息转换成字典,响应给客户端
        dic = {
            'status': '1',
            'user': json.dumps(user.to_dict())
        }
        return HttpResponse(json.dumps(dic))
    else:
        # 判断cookie是否有登录信息
        if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
            # 从cookie中取出数据保存进session
            uid = request.COOKIES['uid']
            uphone = request.COOKIES['uphone']
            request.session['uid'] = uid
            request.session['uphone'] = uphone
            # 根据uid查询对应的user信息转换成字典,响应给客户端
            user = Users.objects.get(id=uid)
            jsonStr = json.dumps(user.to_dict())
            dic = {
                'status': 1,
                'user': jsonStr
            }
            return HttpResponse(json.dumps(dic))
        else:
            # session 和 cookie 中都没有登录信息
            dic = {
                'status': '0',
                'text': '用户尚未登录'
            }
            return HttpResponse(json.dumps(dic))

# 用户退出登录
# 清除 session 和 cookie 中的数据
# 原路返回(request.Meta)
def logout_views(request):
    # 获取请求源地址,如果没有,则返回首页/
    url = request.META.get('HTTP_REFERER', '/')
    resp = redirect(url)
    # 清除 session 中 uid 和 uphone 的数据
    # 判断 session 中是否有登录信息
    if 'uid' in request.session and 'uphone' in request.session:
        del request.session['uid']
        del request.session['uphone']
    # 清除 cookie 中 uid 和 uphone 的数据
    # 判断 cookie 中是否有登录信息
    if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
        resp.delete_cookie('uid')
        resp.delete_cookie('uphone')
    return resp

# 查询出所有的商品类型以及每个类型下的前10个商品
def type_goods_views(request):
    all_list = []
    # 查询所有的商品类型
    types = GoodsType.objects.all()
    for type in types:
        # 将得到的type对象转换成JSON的字符串(字符串中为字典形式)
        type_json = json.dumps(type.to_dict())
        # 获取type下所有的商品(取前10个)
        g_list = type.goods_set.order_by('-price')[0:10]
        # 将前10个商品转化为JSON串
        g_list_json = serializers.serialize('json', g_list)
        # 将type_json 以及 g_list_json封装到一个字典中,再追加到all_list列表中
        dic = {
            'type': type_json,
            'goods': g_list_json,
        }
        all_list.append(dic)
    return HttpResponse(json.dumps(all_list))

# 添加或更新购物车的内容
def add_cart_views(request):
    # 接收数据
    user_id = request.session.get('uid')
    good_id = request.POST['good_id']
    good_count = 1
    # 查看购物车是否有相同的产品,如果有更新数量即可,否则新增数据
    cart_list = CartInfo.objects.filter(
        user_id=user_id, good_id=good_id)
    if cart_list:
        # 已经有商品了,更新数量即可
        cartinfo = cart_list[0]
        cartinfo.ccount = cartinfo.ccount+good_count
        cartinfo.save()
        dic = {
            'status': '1',
            'statusText': '更新数量成功'
        }
        return HttpResponse(json.dumps(dic))
    else:
        # 没有商品,需插入数据到数据库中
        cartinfo = CartInfo()
        cartinfo.good_id = good_id
        cartinfo.user_id = user_id
        cartinfo.ccount = good_count
        cartinfo.save()
        dic = {
            'status': '1',
            'statusText': '添加购物车成功',
        }
        return HttpResponse(json.dumps(dic))

# 某用户购物车内的商品数量
def cart_count_views(request):
    if 'uid' not in request.session:
        dic = {
            'count': 0
        }
        return HttpResponse(json.dumps(dic))
    else:
        uid = request.session['uid']
        all_cart = CartInfo.objects.filter(user_id=uid)
        total_count = 0
        for cart in all_cart:
            total_count += cart.ccount
            dic = {
                'count': total_count
            }
        return HttpResponse(json.dumps(dic))
