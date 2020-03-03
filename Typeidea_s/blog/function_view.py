#coding=utf-8
#__author__ = 'lenovo'







from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from .models import Post , Tag ,Category
from config.models import SideBar
# Create your views here.

'''
使用Model从数据库中批量的拿取数据，然后把标题和摘要展示到页面上
'''
def post_list(request, category_id=None, tag_id=None):
    # content = 'post_list category_id={category_id}, tag_id={tag_id}'.format(
    #     category_id = category_id,
    #     tag_id = tag_id,
    # )
    #
    # return HttpResponse(content)
    tag = None
    category = None

    if tag_id:
        post_list , tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list , category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }

    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context= context)

def post_detail(request, post_id = None):
    # return HttpResponse('detail')
    '''
    在python的函数中和全局同名的变量，如果你有修改变量的值就会变成局部变量，
    在修改之前对该变量的引用自然就会出现没定义这样的错误了，如果确定要引用全局变量，
    并且要对它修改，必须加上global关键字。
    '''
    global  Post
    try:
        post = Post.objects.get(id =post_id)
    except Post.DoesNotExist:
        Post = None
    context ={
        'post':post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)

