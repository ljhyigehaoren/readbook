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


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"

class BookListSerializers(serializers.ModelSerializer):
    category = CategorySerializers()
    isAdd = serializers.SerializerMethodField()

    def get_isAdd(self,row):

        account = self.context['request'].query_params.get('account')
        user = models.UserInfo.objects.filter(account=account).first()
        if user:
            print('=======',user.id,row.id)
            if models.BookStore.objects.filter(book=row.id,user=user.id).count():
                return True
        return False

    class Meta:
        model = models.Book
        fields = "__all__"

class BannderSerializers(serializers.ModelSerializer):
    book = BookListSerializers()
    class Meta:
        model = models.Brand
        fields = "__all__"


class ChpaterListSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Chpater
        fields = "__all__"

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



