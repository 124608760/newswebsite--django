from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from newswebsite.models import Best,Category,Article
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
    context=[]
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

    context=[]
    context={
      "cates":cates,
      "editor_recommendtop3list":editor_recommendtop3list,
      "editor_recommendlist":editor_recommendlist,
      "article_list":article_list
    }


    return render(request,'category.html',context=context)

def login(request):

    return 0

def register(request):

    return 0
def profile(request):

    return 0
def logout(request):

    return 0
