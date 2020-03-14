#__author__ = 'lenovo'
#coding=utf-8
from rest_framework import generics,viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post,Category,Tag
from .serializers import PostSerializer,PostDetailSerializer,\
    CategorySerializer,CategoryDetailSerializer

# '''P244'''
# @api_view()
# def post_list(request):
#     posts = Post.objects.filter(status = Post.STATUS_NORMAL)
#     post_serializers = PostSerializer(posts, many=True)
#     return Response(post_serializers.data)
#
# class PostList(generics.ListAPIView):
#     queryset = Post.objects.filter(status = Post.STATUS_NORMAL)
#     serializer_class = PostSerializer

'''
在Django-rest-framework中提供了更上层的抽象viewset，
用来把这些逻辑都封装起来，让我们在一个类中就能完成所有方法的维护
'''

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status = Post.STATUS_NORMAL)
    # permission_classes = [IsAdminUser] 写入时的权限校验
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class=PostDetailSerializer
        return super().retrieve(request,*args,**kwargs)

    '''获取某个分类下的所有文章'''
    def filter_queryset(self, queryset):
        # 通过获取URL上Query中的category参数
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status = Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request,*args,**kwargs)





