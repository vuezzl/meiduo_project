from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.areas.models import Area


# 获取市和区
class SubAreasView(View):
    def get(self,request,pk):
        sub_data = cache.get('sub_data_'+str(pk))
        if not sub_data:

            # 市和区
            sub_model_list = Area.objects.filter(parent_id=pk)
            # 省
            parent_model = Area.objects.get(id=pk)
            sub_list = []
            for sub in sub_model_list:
                sub_list.append({
                    "id": sub.id,
                    "name": sub.name
                })

            sub_data = {
                "id": parent_model.id,
                "name": parent_model.name,
                "subs":sub_list
            }

            cache.set('sub_data_'+str(pk), sub_data, 3600)


        return JsonResponse({"code":"0","errmsg":"OK",'sub_data': sub_data})









# 获取省
class ProvinceAreasView(View):
    def get(self,request):
        province_list = cache.get('province_list')
        if not province_list:
            # print('判断如果不存在，要去数据库中查找')
            province_model_list = Area.objects.filter(parent_id__isnull=True)
            province_list = []
            for proc in province_model_list:
                province_list.append({
                    "id": proc.id,
                    "name": proc.name
                })
                cache.set(province_list,province_list,3600)
            return JsonResponse({
                      "code":"0",
                      "errmsg":"OK",
                      "province_list":province_list
            })



