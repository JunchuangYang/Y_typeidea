#coding=utf-8
#__author__ = 'lenovo'

from dal import autocomplete
from django import forms

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category,Tag,Post
'''
自定义Form
Model是对数据库中字段的抽象
Form是对用户输入以及Model中要展示的数据的抽象
'''

class PostAdminforms(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=True)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类',
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )
    # 没有上传功能
    #content = forms.CharField(widget=CKEditorWidget(),label='正文', required=True)
    # 有上传功能
    #content = forms.CharField(widget=CKEditorUploadingWidget(),label='正文',required=True)

    '''两种编辑器共存，用户选择使用哪种编辑器'''
    content_ck = forms.CharField(widget=CKEditorUploadingWidget(),label='正文',required=False)
    content_md = forms.CharField(widget=forms.Textarea(),label='正文',required=False)
    content = forms.CharField(widget=forms.HiddenInput(),required=False)


    class Meta:
        model = Post
        fields = (
            'category', 'tag', 'desc', 'title',
             'is_md','content', 'content_md','content_ck',
            'status'
        )

    '''初始化'''
    def __init__(self, instance=None, initial=None, **kwargs):
        '''
        initial就是Form中个字段的初始值，如果是编辑一篇文章，那么instance是当前文章的实例
        '''
        initial = initial or {}
        if instance:
            if instance.is_md:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content

        super().__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        # 获取用户提交的内容
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name, '必填项！')
            return
        self.cleaned_data['content'] = content
        return super().clean()

    class Media:
        js = ('js/post_editor.js', )