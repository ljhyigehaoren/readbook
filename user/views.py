from django.shortcuts import render
from django.http.response import JsonResponse,HttpResponse
import json
# Create your views here.


from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from user import serializers
from user import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from utils import pagination
from django.forms.models import model_to_dict



def login_test(request):
    if request.method == "GET":
        print('get请求')
        return HttpResponse(json.dumps({'code':1000,'data':'get请求'}),content_type='application/json')
    elif request.method == "POST":
        print('post请求')
        return HttpResponse(json.dumps({'code': 1000, 'data': 'post请求'},ensure_ascii=False),content_type='application/json')


############使用序例化####################

class RegisterView(mixins.CreateModelMixin,GenericViewSet):
    """
    account password gender usertype
    """
    queryset = models.UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.errors)
        if self.perform_create(serializer):
            headers = self.get_success_headers(serializer.data)
            return Response({'status':200,'msg':'用户注册成功','data':serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'status':200,'msg':'用户已存在'})
    def perform_create(self, serializer):
        obj = models.UserInfo.objects.filter(account=serializer.validated_data['account']).first()
        if not obj:
            serializer.save()
            return True
        else:
            return False

import hashlib,time
def get_token(account,password):
    """生成用户的登录标示，根据登录的时间和用户名、密码"""
    create_time = str(time.time())
    md5 = hashlib.md5(create_time.encode('utf-8'))
    md5.update(account.encode('utf-8'))
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()

class LoginView(APIView):
    def post(self,request,*args,**kwargs):
        ret = {
            'status':200,
            'msg':None
        }
        try:
            print(request.data)
            obj = models.UserInfo.objects.filter(
                account=request.data['account'],
                password=request.data['password']
            ).first()
            print(obj)
            if not obj:
                ret['status'] = 202
                ret['msg'] = '用户名或密码错误'
            else:
                #创建唯一的token (md5)
                token = get_token(
                    request.data['account'],
                    request.data['password']
                )
                #不存在则创建,存在则更新
                models.Token.objects.update_or_create(
                    user=obj,defaults={'token':token}
                )
                ser = serializers.UserInfoSerializers(instance=obj, many=False)
                data = ser.data
                ret['msg'] = 'successed'
                data['uid'] = token
                ret['data'] = data
                print(ret)

        except Exception as err:
            print(err)
            ret['status'] = 202
            ret['msg'] = '请求异常'

        return Response(ret)

class BannderViewSet(mixins.ListModelMixin,GenericViewSet):
    queryset = models.Brand.objects.all().order_by('index')
    serializer_class = serializers.BannderSerializers

    def list(self, request, *args, **kwargs):
        result = {
            'status': 200,
        }
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            result['data'] = serializer.data

        except Exception as err:
            result['msg'] = '请求异常'

        return Response(result)

class AdvertiseBannderViewSet(mixins.ListModelMixin,GenericViewSet):
    queryset = models.AdvertiseBrand.objects.all().order_by('index')
    serializer_class = serializers.AdvertiseBranderSerializers

    def list(self, request, *args, **kwargs):
        result = {
            'status': 200,
        }
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            result['data'] = serializer.data

        except Exception as err:
            result['msg'] = '请求异常'

        return Response(result)

class CategoryViewSet(mixins.ListModelMixin,GenericViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializers
    pagination_class = pagination.MyPageNumberPagination

    def list(self, request, *args, **kwargs):
        result = {
            'status': 200,
        }
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            result['data'] = serializer.data

        except Exception as err:
            result['msg'] = '请求异常'

        return Response(result)

class RecomendCategoryViewSet(mixins.ListModelMixin,GenericViewSet):
    queryset = models.RecommendCetagory.objects.all().order_by('index')
    serializer_class = serializers.RecomendCategorySerializers
    pagination_class = pagination.MyPageNumberPagination

    def list(self, request, *args, **kwargs):
        result = {
            'status': 200,
        }
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            result['data'] = serializer.data

        except Exception as err:
            result['msg'] = '请求异常'

        return Response(result)


class BookViewSet(mixins.ListModelMixin,GenericViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookListSerializers
    pagination_class = pagination.MyPageNumberPagination


    def list(self, request, *args, **kwargs):
        pid = request.query_params.get('pid')

        if pid and not pid == '(null)':
            queryset = models.Book.objects.filter(category=pid)
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChpaterViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    queryset = models.Chpater.objects.all()
    pagination_class = pagination.MyPageNumberPagination

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ChpaterListSerializers
        return serializers.ChpaterDetailSerializers

    def get_queryset(self):
        if self.action == 'list':
            bookId = self.request.query_params.get('bookId')
            return models.Chpater.objects.filter(book=bookId)
        return self.queryset

class BookStoreViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,
                       mixins.DestroyModelMixin,GenericViewSet):
    queryset = models.BookStore.objects.all()
    pagination_class = pagination.MyPageNumberPagination
    serializer_class = serializers.BookStoreSerializers

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BookStoreListSerializers
        return serializers.BookStoreSerializers

    def list(self, request, *args, **kwargs):
        account = request.query_params.get('account')
        user = models.UserInfo.objects.filter(account=account).first()
        queryset = models.BookStore.objects.filter(user=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        book = models.Book.objects.filter(id=id)
        result = {
            'status':200,
            'msg':'删除成功',
        }
        if book:
            instance = models.BookStore.objects.filter(book=book)
            self.perform_destroy(instance)
            return Response(result,status=status.HTTP_204_NO_CONTENT)
        else:
            result['status'] = 201
            result['msg'] = '删除失败'
        return Response(result,status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = models.UserInfo.objects.filter(account=request.data['user']).first()
        result = {
            'status': 200,
            'msg': '添加成功',
        }
        try:
            if user:
                print(request.data)
                data = {}
                data['user'] = user.id
                data['book'] = request.data['book']
                print(data)
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)

                result['data'] = serializer.data
                print(result)
                return Response(result, status=status.HTTP_201_CREATED, headers=headers)
            else:
                result['status'] = 201
                result['msg'] = '添加失败'
                return Response(result, status=status.HTTP_200_OK)
        except Exception as err:
            result['status'] = 201
            result['msg'] = '添加失败'
            return Response(result, status=status.HTTP_200_OK)

class UserProfileViewSet(mixins.RetrieveModelMixin,GenericViewSet):

    queryset = models.UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializers

    def retrieve(self, request, *args, **kwargs):
        result = {
            'status':200,
        }
        try:
            account = request.query_params.get('account')
            instance = models.UserInfo.objects.filter(account=account).first()
            serializer = self.get_serializer(instance)
            result['data'] = serializer.data
        except Exception as err:
            result['status'] = 201
            result['msg'] = '用户详情获取失败'
        return Response(result)
























