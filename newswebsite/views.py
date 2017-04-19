from django.contrib.auth.decorators import login_required
from django.shortcuts import render,Http404, redirect, HttpResponse
from django.contrib.auth import authenticate,login as user_login,logout as user_logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from newswebsite.models import *
from newswebsite.forms import *
# Create your views here.
def index(request):
    cates = Category.objects.all().order_by("-id") #分类列表

    todaynew_big = Best.objects.filter(select_reason="今日新闻")[0].select_article #取出一篇今日新闻作为大标题
    todaynew = Best.objects.filter(select_reason="今日新闻")[:3]
    todaynew_top3 = [i.select_article for i in todaynew]                          #取出三篇今日新闻

    index_recommend = Best.objects.filter(select_reason="首页推荐")[:4]
    index_recommendlist = [i.select_article for i in index_recommend]   #取出四篇首页推荐

    editor_recommendtop3 = Best.objects.filter(select_reason="编辑推荐")[:3]
    editor_recommendtop3list = [i.select_article for i in editor_recommendtop3] #取出三篇编辑推荐作为大标题

    editor_recommend = Best.objects.filter(select_reason="编辑推荐")[3:10]
    editor_recommendlist = [i.select_article for i in editor_recommend]     #再取出七篇编辑推荐

    article_list = Article.objects.all().order_by("-publish_time") #取出所有文章
    pagerobot = Paginator(article_list,5)                         #创建分页器，每页限定五篇文章
    page_num = request.GET.get("page",1)                            #取到当前页数
    try:
        article_list = pagerobot.page(page_num)                   #一般情况下返回当前页码下的文章
    except EmptyPage:
        article_list = pagerobot.page(pagerobot.num_pages)        #如果不存在该业，返回最后一页
    except PageNotAnInteger:
        article_list = pagerobot.page(1)                          #如果页码不是一个整数，返回第一页
    context={}
    context={
      "cates":cates,
      "todaynew_big":todaynew_big,
      "todaynew_top3":todaynew_top3,
      "index_recommendlist":index_recommendlist,
      "editor_recommendtop3list":editor_recommendtop3list,
      "editor_recommendlist":editor_recommendlist,
      "article_list":article_list
    }


    return render(request,'index.html',context=context)
def category(request,cate_id):
    cates = Category.objects.all().order_by("-id") #分类列表

    editor_recommendtop3 = Best.objects.filter(select_reason="编辑推荐")[:3]
    editor_recommendtop3list = [i.select_article for i in editor_recommendtop3] #取出三篇编辑推荐作为大标题

    editor_recommend = Best.objects.filter(select_reason="编辑推荐")[3:10]
    editor_recommendlist = [i.select_article for i in editor_recommend]     #再取出七篇编辑推荐

    article_list = Article.objects.filter(category=int(cate_id)).order_by("-publish_time") #取出当前目录下的所有文章
    print(article_list[0].category)
    pagerobot = Paginator(article_list,5)                         #创建分页器，每页限定五篇文章
    page_num = request.GET.get("page",1)                            #取到当前页数
    try:
        article_list = pagerobot.page(page_num)                   #一般情况下返回当前页码下的文章
    except EmptyPage:
        article_list = pagerobot.page(pagerobot.num_pages)        #如果不存在该业，返回最后一页
    except PageNotAnInteger:
        article_list = pagerobot.page(1)                          #如果页码不是一个整数，返回第一页

    context={}
    context={
      "cates":cates,
      "editor_recommendtop3list":editor_recommendtop3list,
      "editor_recommendlist":editor_recommendlist,
      "article_list":article_list
    }


    return render(request,'category.html',context=context)
def detail(request,article_id):
    cates = Category.objects.all().order_by("-id") #分类列表

    editor_recommendtop3 = Best.objects.filter(select_reason="编辑推荐")[:3]
    editor_recommendtop3list = [i.select_article for i in editor_recommendtop3] #取出三篇编辑推荐作为大标题

    editor_recommend = Best.objects.filter(select_reason="编辑推荐")[3:10]
    editor_recommendlist = [i.select_article for i in editor_recommend]     #再取出七篇编辑推荐

    article = Article.objects.get(id=article_id)

    comments = Comment.objects.filter(belong_article=article)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            words = form.cleaned_data.get("comment")
            comment = Comment(belong_user=request.user,words=words,belong_article=Article.objects.get(id=article_id))
            comment.save()
            form = CommentForm()

    context ={}
    context ={
       "cates":cates,
       "editor_recommendtop3list":editor_recommendtop3list,
       "editor_recommendlist":editor_recommendlist,
       "article":article,
       "comments":comments,
       "form":form
    }

    return render(request,'detail.html',context=context)

def login(request):
    if request.method == 'GET':
        form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username,password=password)
            if user:
                user_login(request,user)              #由于login方法和我自定义的login视图重名，这里将django.contrib.auth中的login方法重命名为user_login导入
                return redirect(to='index')
            else:
                return HttpResponse('用户名不存在或用户名密码错误')

    context={}
    context['form'] = form

    return render(request,'login.html',context=context)

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
           username = form.cleaned_data.get("username")
           email = form.cleaned_data.get("email")
           password = form.cleaned_data.get("password")
           user = User(username=username,email=email)
           user.set_password(password)
           user.save()                                                         #创建用户保存
           userprofile = UserProfile(belong_to=user,avatar='avatar/avatar.png')
           userprofile.save()                                                  #创建该用户的资料
           return redirect(to='login')

    context={}
    context['form']=form

    return render(request,'register.html',context=context)

@login_required(login_url='login')              #未登录则跳转到登录页面
def profile(request):
    if request.method == 'GET':
        form = EditForm(initial={'username':request.user.username,'email':request.user.email})
    if request.method == 'POST':
        form = EditForm(request.POST,request.FILES)

        if form.is_valid():
           user = request.user
           email = form.cleaned_data.get("email")
           password = form.cleaned_data.get("password")
           avatar = form.cleaned_data.get("avatar")
           user.email = email
           if avatar:
                user_profile = UserProfile.objects.get(belong_to=user)
                user_profile.avatar = avatar
                user_profile.save()             #如果有上传头像，替换用户的头像
           user.set_password(password)
           user.save()
           return redirect(to='login')

    context={}
    context['form']=form

    return render(request,'profile.html',context=context)

def logout(request):
    user_logout(request)

    return redirect(to='login')
