#coding=utf-8
'''编写 class-based view 代码'''
from datetime import date

from django.db.models import Q, F
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .models import Post , Tag ,Category

from config.models import SideBar
from comment.forms import CommentForm
from comment.models import Comment

'''通用数据：分类导航、侧边栏、底部导航'''
class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())

        return context

    # def get_sidebars(self):
    #     return SideBar.objects.filter(status=SideBar.STATUS_SHOW)
    #
    # def get_navs(self):
    #     categories = Category.objects.filter(status=Category.STATUS_NORMAL)
    #     nav_categories = []
    #     normal_categories = []
    #     for cate in categories:
    #         if cate.is_nav:
    #             nav_categories.append(cate)
    #         else:
    #             normal_categories.append(cate)
    #
    #     return {
    #         'navs': nav_categories,
    #         'categories': normal_categories,
    #     }

'''首页'''
class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


'''分类列表页'''
class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        '''self.kwargs中的数据是从定义的URL中获得的'''
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category' : category
        })
        return context

    def get_queryset(self):
        '''重写queryset，根据分类过滤'''
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id = category_id)


'''标签列表页'''
class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk = tag_id)
        context.update({
            'tag':tag
        })

    def get_queryset(self):
        '''重写queryset，根据标签过滤'''
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id = tag_id)

'''博文详情页'''
class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    '''
    使用comment_block代替以下代码
    '''
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'comment_form':CommentForm,
    #         'comment_list':Comment.get_by_target(self.request.path),
    #     })
    #     return context

    # #文章访问统计
    # def get(self, request, *args, **kwargs):
    #     response = super().get(request, *args, **kwargs)
    #     Post.objects.filter(pk = self.object.id).update(pv=F('pv')+1, uv=F('uv')+1)
    #     # 调试用，打印SQL语句
    #     from django.db import connection
    #     print(connection.queries)
    #     return response

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)  # 1分钟有效

        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60)  # 24小时有效

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)

'''关键词搜索页'''
class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword', '')
        })
        return context
    '''
    覆写了父类的 get_queryset 方法。该方法默认获取指定模型的全部列表数据。
    为了获取指定分类下的文章列表数据，我们覆写该方法，改变它的默认行为。
    '''
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        # 因此我们可以判断，contains是精确查询，icontains是忽略大小写的模糊查询
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)



