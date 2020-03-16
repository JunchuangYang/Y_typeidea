#coding=utf-8
#__author__ = 'lenovo'

from django.contrib.admin import AdminSite

'''编写用户模块的管理'''

class CustomSite(AdminSite):
    site_header = 'Typeidea'
    site_title = 'Typeidea 管理后台'
    index_title = '首页'

custom_site = CustomSite(name='cus_admin')