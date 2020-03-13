#coding=utf-8
#__author__ = 'lenovo'

from django.contrib import admin

class BaseOwnerAdmin(object):
    """
    1. 用来处理文章、分类、标签、侧边栏、友链这些model的owner字段自动补充
    2. 用来针对queryset过滤当前用户的数据
    """

    exclude = ('owner', )

    # django admin 的方法
    # def get_queryset(self, request):
    #     qs = super(BaseOwnerAdmin, self).get_queryset(request)
    #     return qs.filter(owner = request.user)
    #
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    # xadmin中的方法
    def  get_list_queryset(self):
        request = self.request
        qs = super(BaseOwnerAdmin, self).get_list_queryset()
        return qs.filter(owner = request.user)

    def save_models(self):
        self.new_obj.owner = self.request.user
        return super().save_models()