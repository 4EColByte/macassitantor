#!/usr/bin/env python
# coding: utf-8
# @Created     : 2019/9/23 10:25
# @Author      : zhuchhui
# @Email       : zhuchhui@ewell.cc
# @Description : 
# @Other:
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('test', test, name='test'),
    path('departdetails/<int:dpt_id>', DptMemberDetails.as_view(), name='departdetails'),
    path('membertails/<int:level>', MemberView.as_view(), name='memberdetails'),
    path('addmember/<int:dpt_id>', MemberView.as_view(), name='addmember'),
    path('delmember/<int:mmb_id>', delmember, name='delmember'),
    path('updatemember/<int:mmb_id>', updatemember, name='upatemember'),
    path('departinfo/<int:dpt_id>', DepartmentView.as_view(), name='departmentinfo'),
    path('adddpt', adddepartment, name='adddepartment'),
    path('deldpt/<int:dpt_id>', adddepartment, name='removedepartment'),
    path('macinfo/<int:mmb_id>', MacView.as_view(), name='macinfo'),
    path('addmac/<int:mmb_id>', addmac, name='addmac'),
    path('delmac/<int:mac_id>', delmac, name='delmac'),
    path('updatemac/<int:mac_id>', updatemac, name='upatemac'),
    path('departmng', departmanage, name='dptmng'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('jsonrsp/', jsonrsp, name='logout'),
    path('jsondata/', jsondata, name='jsondata'),
    path('dptpages/', dptpages, name='dptpages'),
]
