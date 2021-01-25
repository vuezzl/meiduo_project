from django.urls import  converters
# 用户名路由转换器
class UsenameConverter:
    regex = '[a-zA-Z0-9_-]{5,20}'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)


# 手机号路由转换器
class MobileConverter:
    regex = '1[3-9]\d{9}'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)

