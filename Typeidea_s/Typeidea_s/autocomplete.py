#__author__ = 'lenovo'
#coding=utf-8


from dal import autocomplete

from blog.models import Category,Tag

'''
自动补全接口
'''
class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # 判断用户是否登录
        if not self.request.user.is_authenticated():
            return Category.objects.none()
        # 获取该用户创建的所有分类
        qs = Category.objects.filter(owner = self.request.user)
        # 判断是否存在self.q,这里的q就是URL参数上传过来的值，在使用name_istartwith进行查询
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Tag.objects.none()
        # 获取该用户创建的所有标签
        qs = Tag.objects.filter(owner=self.request.user)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs










