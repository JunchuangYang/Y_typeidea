#__author__ =
#coding=utf-8
from rest_framework import serializers,pagination

from .models import Post,Category,Tag

'''序列化数据

PostSetializer中可以继续实现自定义字段，自定义校验逻辑，自定义数据处理逻辑等方法
'''

class PostSerializer(serializers.HyperlinkedModelSerializer):

    # SlugRelatedField外键数据需要通过它来配置
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',# 用来展示字段是什么
    )

    tag = serializers.SlugRelatedField(
        many=True,#多对多
        read_only=True,
        slug_field='name',
    )

    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    # 以上是文章列表接口需要的Serializer


    class Meta:
        model = Post
        fields = ['id','title', 'category','tag','owner', 'created_time']
        extra_kwargs = {
            'url': {'view_name': 'api-post-detail'}
        }

'''文章详情接口需要的Serializer'''
class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'category','tag','owner',
                    'content_html', 'created_time']



'''分类页'''
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id','name','created_time',
        )

'''分类详情页'''
class CategoryDetailSerializer(CategorySerializer):
    '''
    serializers.SerializerMethodField:帮我们把posts字段获取的内容映射到paginated_posts方法上，
    也就是最终返回的数据中，posts对应的数据需要通过paginated_posts来获取
    '''
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'created_time', 'posts'
        )



