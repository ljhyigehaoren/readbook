"""
    限制请求的频率
"""
from rest_framework.throttling import BaseThrottle,SimpleRateThrottle
import time

VISIT_RECORD = {}

class MyThrottle(BaseThrottle):

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        """
        判断是否可以继续访问接口，True：可以继续访问     False：访问频率太高，请求被限制
        :param request:
        :param view:
        :return:
        """
        # 获取用户的ip地址
        remote_addr = request.META.get("REMOTE_ADDR")
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime,]
        history = VISIT_RECORD.get(remote_addr)
        self.history = history

        while history and history[-1] < ctime - 60:
            history.pop()

        if len(history) < 3:
            history.insert(0,ctime)
            return True

    def wait(self):
        """可以设置提示，也可以返回等待的时间"""
        ctime = time.time()

        return 60 - (ctime - self.history[-1])

class MySimpleRateThrottle(SimpleRateThrottle):
    """限制接口的请求频率"""
    scope = "readbook"

    def get_cache_key(self, request, view):
        return self.get_ident(request)



