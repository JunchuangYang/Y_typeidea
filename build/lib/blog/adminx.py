#coding=utf-8
from django.contrib import admin
from django.urls import reverse
from django.utils.html import  format_html
from django.contrib.admin.models import LogEntry

import xadmin
from xadmin.filters import manager
from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import RelatedFieldListFilter

from .models import Post,Tag,Category
from .adminforms import PostAdminforms
from Typeidea_s.base_admin import BaseOwnerAdmin
from Typeidea_s.custom_site import custom_site

# Register your models here.


'''在同一页面关联编辑数据'''
class PostInline:
    form_layout = (
        Container(
            Row("title", "desc"),
        )
    )
    extra = 1  # 控制额外多几个
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):


    inlines = [PostInline, ]

    list_display = ('name', 'status', 'is_nav', 'post_count','created_time')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(RelatedFieldListFilter):
    # 作用：确认字段是否需要被当前的过滤器处理
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')

    '''
    自定义过滤器只展示当前用户分类
    P124
    '''
    #
    # title = '分类过滤器'
    #
    # # 查询时URL参数的名字
    # parameter_name = 'owner_category'
    #
    # def lookups(self, request, model_admin):
    #     return Category.objects.filter(owner=request.user).values_list('id', 'name')
    #
    # def queryset(self, request, queryset):
    #     category_id = self.value()
    #     if category_id:
    #         return queryset.fliter(category_id = self.value())
    #     return queryset

manager.register(CategoryOwnerFilter, take_priority=True)

@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):

    '''自定义Form'''
    form = PostAdminforms

    # 配置列表页展示字段，operator为自定义字段
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator'
    ]
    list_display_links = []

    #自定义过滤器，让用户只能看见自己所创建的类别
    list_filter = ['category']


    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    # 指定字段不展示
    exclude = ('owner',)

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    '''
    fieldsets用来控制布局， P125
    classes:给要配置的模块加上css属性，Django默认collapse和wide
    ():元祖
    []:列表
    {}:字典
    '''
    # fieldsets = (
    #     ('基础配置', {
    #         'description':'基础配置描述',
    #         'fields':(
    #             ('title','category'),
    #             'status',
    #         ),
    #     }),
    #     ('内容',{
    #         'fields':(
    #             'desc',
    #             'content',
    #         ),
    #     }),
    #     ('额外信息',{
    #         'classes':('wide',),
    #         'fields':('tag', ),
    #     })
    # )
    '''xadmin样式控制'''
    form_layout = (
            Fieldset(
                '基础信息',
                Row("title", "category"),
                'status',
                'tag',
            ),
            Fieldset(
                '内容信息',
                'desc',
                'is_md',
                'content_ck',
                'content_md',
                'content',
            )
        )

    # 多对多字段展示的配置filter_horizontal和filter_vertical
    filter_horizontal = ('tag',)
    #filter_vertical = ('tag',)


    # operator为自定义字段，与list_display对应
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args={obj.id,})
        )
    # 指定表头的展示文案
    operator.short_description = '操作'


    '''
    我们可以通过自定义Media类来往页面上添加JavaScript和CSS资源
    '''
    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )


    # def get_media(self):
        # # xadmin基于bootstrap，引入会页面样式冲突，仅供参考, 故注释。
        # media = super().get_media()
        # media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
        # media.add_css({
            # 'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
        # })
        # return media

'''在admin上查看操作日志'''
# @admin.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']

