#coding=utf-8
"""Typeidea_s URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog.views import IndexView,CategoryView,TagView,PostDetailView


from config.views import links
from .custom_site import custom_site

'''
P142
url的定义理解为一个路径（正则字符串）对一个函数的映射
url(<正则字符串>,<view function>, <固定参数contentxt>, <url的名称>)

?P<value>:就是命名一个名字为value的组，匹配规则符合后面的/d+


funtionView URL的写法

urlpatterns = [
    url(r'^$', post_list),
    url(r'^category/(?P<category_id>\d+)/$', post_list, name= 'category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', post_list, name= 'tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', post_detail, name= 'post-detail'),
    url(r'^links/$', links, name= 'links'),

    url(r'^super_admin/', admin.site.urls, name= 'super-admin'),
    url(r'^admin/', custom_site.urls, name= 'admin')
]
'''

# class-based view URL写法
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name= 'category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view() , name= 'tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name= 'post-detail'),
    url(r'^links/$', links, name= 'links'),

    url(r'^super_admin/', admin.site.urls, name= 'super-admin'),
    url(r'^admin/', custom_site.urls, name= 'admin')
]












