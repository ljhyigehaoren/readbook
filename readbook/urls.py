"""readbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
# from django.contrib import admin
from user import views as userview
from rest_framework.routers import DefaultRouter
import xadmin

router = DefaultRouter()
router.register(r'book',userview.BookViewSet,base_name='book')
router.register(r'category',userview.CategoryViewSet,base_name='category')
router.register(r'rcategory',userview.RecomendCategoryViewSet,base_name='rcategory')
router.register(r'banner',userview.BannderViewSet,base_name='banner')
router.register(r'adbanner',userview.AdvertiseBannderViewSet,base_name='adbanner')
router.register(r'chpater',userview.ChpaterViewSet,base_name='chpater')
router.register(r'bookstore',userview.BookStoreViewSet,base_name='bookstore')

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^register/$',userview.RegisterView.as_view({'post':'create'})),
    url(r'^login/$',userview.LoginView.as_view()),
    url(r'',include(router.urls)),
    url(r'userprofile/',userview.UserProfileViewSet.as_view({'get':'retrieve'})),
    url(r"^logintest/",userview.login_test),
]
