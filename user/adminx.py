import xadmin
from xadmin import views

from user.models import UserInfo,Category,Book,Chpater,RecommendCetagory,Brand,BookStore

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "说世界"
    site_footer = "说世界"


class UserInfoAdmin(object):
    list_display = ['account','password','gender','usertype','birthday']

class BookCategoryAdmin(object):
    list_display = ['name','info','coverImage']

class BookInfoAdmin(object):
    search_fields = ['title']
    list_filter = ['category']
    list_display = ['title','info','author','category','stauts','coverImage','readNum','addTime']

class ChpterInfoAdmin(object):
    search_fields = ['title']
    list_display = ['title','size','type','content','readNum','addTime','book']

class BrandAdmin(object):
    list_display = ['book','index','addTime']

class RecommendCetagoryAdmin(object):
    list_display = ['category','index','addTime']

class BookStoreAdmin(object):
    list_display = ['book','user','addTime']



xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

xadmin.site.register(UserInfo,UserInfoAdmin)
xadmin.site.register(Category,BookCategoryAdmin)
xadmin.site.register(Book,BookInfoAdmin)
xadmin.site.register(Chpater,ChpterInfoAdmin)
xadmin.site.register(Brand,BrandAdmin)
xadmin.site.register(RecommendCetagory,RecommendCetagoryAdmin)
xadmin.site.register(BookStore,BookStoreAdmin)

