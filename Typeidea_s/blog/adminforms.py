#coding=utf-8
#__author__ = 'lenovo'

from django import forms

'''
自定义Form
Model是对数据库中字段的抽象
Form是对用户输入以及Model中要展示的数据的抽象
'''

class PostAdminforms(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=True)
