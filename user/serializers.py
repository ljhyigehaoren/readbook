from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from user import models
import re

class UserInfoSerializers(serializers.ModelSerializer):
    birthday = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = models.UserInfo
        fields = "__all__"

    #自定义验证字段的方法
    def validate_account(self,account):

        #通过正则表达式验证手机号是否正确
        result = re.match('^1[358769]\d{9}',account)
        if not result:
            #手机号验证未通过，返回错误信息
            raise ValidationError('手机号非法')
        #验证通过，返回手机号
        return account

    def validate_password(self,password):

        #通过正则表达式验证手机号是否正确
        result1 = re.match('[A-Z]',password)
        result2 = re.search('[A-Za-z]', password)
        result3 = re.search('[0-9]', password)
        if result1 and result2 and result3:
            # 验证通过，返回手机号
            return password
        else:
            # 8427f6c12b6226296aa6b6f5e0c04347
            #手机号验证未通过，返回错误信息（必须大写字母开头，包含大写或者小写字母及数字）
            raise ValidationError('密码不符合规范')



class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"

class RecomendCategorySerializers(serializers.ModelSerializer):
    id = serializers. IntegerField(source='category.id')
    name = serializers.CharField(source='category.name')
    info = serializers.CharField(source='category.info')
    coverImage = serializers.CharField(source='category.coverImage')

    class Meta:
        model = models.RecommendCetagory
        fields = ['id','name','info','coverImage']


class BookListSerializers(serializers.ModelSerializer):
    addTime = serializers.DateTimeField('%Y-%m-%d %H:%M')
    url = serializers.HyperlinkedIdentityField(lookup_field ="id",lookup_url_kwarg="pk",view_name ="book-detail")

    # 根据接口需要，书籍列表是否需要返回分类信息，使用category = CategorySerializers()表示序列化所有分类参数
    # category = CategorySerializers()

    # 自定义category返回的数据
    category = serializers.SerializerMethodField()

    #自定义分类参数
    def get_category(self,row):
        # row -> Book
        return {"id":row.category.id,"name":row.category.name}

    class Meta:
        model = models.Book
        fields = "__all__"

class BookDetailSerializers(serializers.ModelSerializer):
    addTime = serializers.DateTimeField('%Y-%m-%d %H:%M')
    # 根据接口需要，使用category = CategorySerializers()表示序列化所有分类参数
    category = CategorySerializers()
    #判断该书籍是否被用户添加至书架中
    isAdd = serializers.SerializerMethodField()
    def get_isAdd(self, row):
        account = self.context['request'].query_params.get('account')
        user = models.UserInfo.objects.filter(account=account).first()

        if user:
            print('=======', user.id, row.id)
            if models.BookStore.objects.filter(book=row.id, user=user.id).count():
                return True
        return False

    class Meta:
        model = models.Book
        fields = "__all__"

class BookBonnerSerializers(serializers.ModelSerializer):
    addTime = serializers.DateTimeField('%Y-%m-%d %H:%M')
    url = serializers.HyperlinkedIdentityField(lookup_field ="id",lookup_url_kwarg="pk",view_name ="book-detail")

    class Meta:
        model = models.Book
        fields = ["addTime","url","id","title","coverImage","readNum","info"]

class BannderSerializers(serializers.ModelSerializer):
    book = BookBonnerSerializers()
    class Meta:
        model = models.Brand
        fields = ["id","book","index"]

class AdvertiseBranderSerializers(serializers.ModelSerializer):
    addTime = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = models.AdvertiseBrand
        fields = "__all__"

class ChpaterListSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Chpater
        fields = ["id","title","type"]

class ChpaterDetailSerializers(serializers.ModelSerializer):
    book = BookListSerializers()
    class Meta:
        model = models.Chpater
        fields = "__all__"

class BookStoreSerializers(serializers.ModelSerializer):

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=models.BookStore.objects.all(),
                fields=['book', 'user'],
                message='已加入书架'
            )
        ]
        model = models.BookStore
        fields = ['book','user']

class BookStoreListSerializers(serializers.ModelSerializer):
    book = BookListSerializers()
    # user = UserInfoSerializers()
    addTime = serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H-%M")
    class Meta:
        model = models.BookStore
        fields = "__all__"



