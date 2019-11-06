#!/usr/bin/env python
# coding: utf-8
# @Created     : 2019/9/23 8:33
# @Author      : zhuchhui
# @Email       : zhuchhui@ewell.cc
# @Description : 
# @Other:
from django import forms
from .models import Department

LEVEL_CHOICE = ((1, "一级部门"), (2, "二级部门"), (3, "特殊地址"))
class DepaartmentForm(forms.Form):
    name = forms.CharField(max_length=40, label='部门名称',
                           widget=forms.TextInput(attrs={
                               "class": "layui-input",
                               "placeholder": "填写部门名称",
                               "lay-verify": "required",
                               "autocomplete": "off"}),
                           required=True)
    level = forms.ChoiceField(choices=LEVEL_CHOICE, label='部门级别',
                              widget=forms.Select(choices=LEVEL_CHOICE, attrs={}),
                             )
    comments = forms.CharField(max_length=60, label='部门简介',
                              widget=forms.Textarea(
                                  attrs={"placeholder":"添加备注或部门描述",
                                         "class": "layui-textarea"})
                              )


class MemberForm(forms.Form):
    name = forms.CharField(max_length=40, label='姓名', error_messages={'required':'用户名不能为空'})
    phone = forms.CharField(max_length=11, label='手机')
    departid = forms.IntegerField(label='部门')
    comment = forms.CharField(label='备注', widget=forms.Textarea, max_length=120)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'layui-input', 'style': 'width: 200px;', "lay-verify": "required"})
        self.fields['phone'].widget.attrs.update({'class': 'layui-input', 'style': 'width: 200px;', "lay-verify": "phone|number"})
        self.fields['comment'].widget.attrs.update({'class': 'layui-textarea', 'style': 'height: 20px; width:80%;'})
        # self.fields['depart'].widget.attrs.update({'class': 'layui-input-inline'})
        # self.fields['depart'].choices=Department.objects.all().values_list('id', 'name')

MACTYPE_CHOICES = (
  (1, '有线'),
  (2, '无线'),
  (3, '其他'),
)

class PersonalMac(forms.Form):
    mactype = forms.ChoiceField(choices=MACTYPE_CHOICES, label='Mac类型')
    phaddr = forms.CharField(max_length=17, label='Mac地地址')
    comment = forms.CharField(widget=forms.Textarea, max_length=120, label='备注')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mactype'].widget.attrs.update({'class': 'layui-input', 'style': 'width: 200px;', "lay-verify": "required"})
        self.fields['phaddr'].widget.attrs.update({'class': 'layui-input', 'style': 'width: 200px;', "lay-verify": "phone|number"})
        self.fields['comment'].widget.attrs.update({'class': 'layui-textarea', 'style': 'height: 60px; width:80%;'})

class PubMac(forms.Form):
    mactype = forms.ChoiceField(choices=MACTYPE_CHOICES, label='Mac类型')
    macaddr = forms.CharField(max_length=16, label='Mac地地址')
    comment = forms.CharField(widget=forms.Textarea, max_length=120, label='备注')


class Login(forms.Form):
    name =  forms.CharField(max_length=16, label='用户', required=True)
    passwd = forms.CharField(widget=forms.PasswordInput, max_length=30, label='密码', required=True)