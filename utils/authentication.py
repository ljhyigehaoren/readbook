from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from user import models
class MyAuthentication(BaseAuthentication):

    def authenticate(self, request):
        uid = request.query_params.get("uid")
        obj = models.Token.objects.filter(token=uid).first()
        if not obj:
            raise exceptions.AuthenticationFailed("用户未登录，或登录失效")
        return (obj.user,uid)



