from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# 分类表
class Category(models.Model):
    name = models.CharField(max_length=40, null=False)  # 分类名

    def __str__(self):
        return self.name


# 文章表
class Article(models.Model):
    title = models.CharField(max_length=100, null=False)  # 标题
    intro = models.CharField(max_length=1000)  # 导语
    abstract = models.TextField()  # 摘要
    category = models.ForeignKey(Category, related_name="cate") #连接分类表的外键，多对一关系
    content = models.TextField(null=False)  # 内容
    publish_time = models.DateTimeField(null=False, default=now)  # 发布时间
    image = models.FileField(upload_to='article_image')  # 文章配图
    source_link = models.CharField(max_length=200)  # 原文链接
    author_name = models.CharField(max_length=100, null=False)  # 作者名字
    author_avatar = models.FileField(upload_to='author_avatar')  # 作者头像
    author_desc = models.CharField(max_length=100, null=False)  # 作者签名

    def __str__(self):
        return self.title    #在后台中以文章标题显示


# 精选文章
class Best(models.Model):
    select_article = models.ForeignKey(Article, related_name='select_article')  # 被精选的文章
    SELECT_REASON = (
        ('今日新闻', '今日新闻'),
        ('首页推荐', '首页推荐'),
        ('编辑推荐', '编辑推荐')
    )
    select_reason = models.CharField(choices=SELECT_REASON, max_length=50, null=False)  # 精选的理由

    def __str__(self):
        return self.select_reason + '-' + self.select_article.title


# 用户信息表
class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name="profile")  # 所属用户
    avatar = models.FileField(upload_to='avatar')  # 用户头像

    def __str__(self):
        return self.belong_to.username


# 评论表
class Comment(models.Model):
    belong_article = models.ForeignKey(Article, related_name='article')  # 评论所属的文章
    belong_user = models.ForeignKey(User, related_name='user')  # 评论者
    words = models.CharField(max_length=200, null=False)  # 评论内容
    created = models.DateTimeField(null=False, default=now)  # 评论时间

    def __str__(self):
        return self.belong_user.username + ': ' + self.words
