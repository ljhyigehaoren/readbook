from django.db import models
from datetime import datetime
# Create your models here.


class UserInfo(models.Model):
    GENDER_TYPE = (
        (1,'男'),
        (2,'女'),
    )
    USER_TYPE = (
        (1,'普通用户'),
        (2,'VIP')
    )
    account = models.CharField(max_length=11,unique=True,verbose_name='账户')
    password = models.CharField(max_length=25,verbose_name='密码')
    gender = models.IntegerField(choices=GENDER_TYPE,default=1,verbose_name='性别')
    usertype = models.IntegerField(choices=USER_TYPE,default=1,verbose_name='用户类型')
    birthday = models.DateTimeField(default=datetime.now,verbose_name='出生年月')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.account

class Token(models.Model):
    # 唯一的，标示用户是否登录
    token = models.CharField(max_length=256)
    # 用户与token之间是一对一的关系
    user = models.OneToOneField(UserInfo)


    class Meta:
        verbose_name = '用户token'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.account


class Category(models.Model):
    name = models.CharField(max_length=128,null=False,blank=False,verbose_name='分类名称')
    info = models.CharField(max_length=256, null=True, blank=True, verbose_name='分类描述')
    coverImage = models.CharField(max_length=256, null=True,
                                  blank=True,
                                  verbose_name='分类封面图'
                                  )
    class Meta:
        verbose_name = '小说分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(Category, verbose_name='所属分类',related_name='category')
    title = models.CharField(max_length=128,null=False,blank=False,verbose_name='书籍名称')
    info = models.CharField(max_length=256, null=False, blank=False, verbose_name='书籍简介')
    author = models.CharField(max_length=20, null=False, blank=False, verbose_name='作者')
    stauts = models.CharField(max_length=20, null=False, blank=False, verbose_name='状态')
    coverImage = models.CharField(max_length=256, null=False, blank=False, verbose_name='书籍封面')
    readNum = models.IntegerField(default=0,verbose_name='浏览量')

    addTime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '小说书籍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Chpater(models.Model):
    CHPATER_TYPE = (
        (1, '限免'),
        (2, 'VIP')
    )
    book = models.ForeignKey(Book, verbose_name='书籍')
    title = models.CharField(max_length=128, null=False, blank=False, verbose_name='章节名称')
    size = models.IntegerField(verbose_name='字数')
    type = models.IntegerField(default=1,choices=CHPATER_TYPE,null=False,blank=False,verbose_name='是否是VIP章节')
    content = models.TextField(verbose_name='章节内容')
    readNum = models.IntegerField(default=0, verbose_name='浏览量')

    addTime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '小说章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Brand(models.Model):
    book = models.ForeignKey(Book)
    index = models.IntegerField()

    addTime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book.title

class AdvertiseBrand(models.Model):
    title = models.CharField(max_length=56)
    index = models.IntegerField()
    info = models.CharField(max_length=256)
    coverImage = models.CharField(max_length=256,null=False,blank=True)
    url = models.CharField(max_length=256,null=False,blank=True)
    addTime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '广告轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class RecommendCetagory(models.Model):
    category = models.ForeignKey(Category)
    index = models.IntegerField()

    addTime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')


    class Meta:
        verbose_name = '推荐分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name


class BookStore(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(UserInfo)

    addTime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        unique_together = ("book", "user")
        verbose_name = '用户书架'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book.title





