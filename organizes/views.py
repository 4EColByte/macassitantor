from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib import auth
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .forms import DepaartmentForm, MemberForm, PersonalMac, Login
from .models import Member, Department, MacAddr, User


# Create your views here.
class DepartmentView(View):
    def get(self, request, *args, **kwargs):
        dpt_id = kwargs['dpt_id']
        objects_filter = Department.objects.get(id=dpt_id)
        depart = objects_filter
        print(depart.parent)
        rpsdata = {"depart": depart}
        return render(request, "departdetail.html", rpsdata)

    def post(self, request, *args, **kwargs):
        form = DepaartmentForm()
        return render(request, 'departadd.html', {'form': form})


class DptMemberDetails(View):
    def get(self, request, *args, **kwargs):
        dpt_id = kwargs['dpt_id']
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        memebers_obj = Member.objects.filter(depart_id=dpt_id)
        # paginator = Paginator(memebers_obj, limit)
        memberform = MemberForm()
        macdetail = {}
        if memebers_obj:
            for member in memebers_obj:
                macs = MacAddr.objects.filter(member=member)
                macdetail[member] = macs
        rpsdata = {'dptid': dpt_id, "macinfo": macdetail, 'form': memberform}
        return render(request, "departdetails.html", rpsdata)

    def post(self, request, *args, **kwargs):
        dpt_id = kwargs['dpt_id']


def adddepartment(request):
    if request.method == "POST":
        form = DepaartmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            level = form.cleaned_data['level']
            comments = form.cleaned_data['comments']
            print(name, level, comments)
            depart = Department(name=name, level=level, comments=comments)
            depart.save()
            return JsonResponse({'code': 1, 'msg': '保存成功'})
    else:
        form = DepaartmentForm()
        return render(request, 'departadd.html', {'form': form})


class MemberView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        form = MemberForm()
        return render(request, 'memberdetails.html', {"conten": member_details})

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            comment = form.cleaned_data['comment']
            depatid = form.cleaned_data['departid']
            depart = Department.objects.filter(id=depatid).first()
            member = Member(name=name, phone=phone, depart=depart, comment=comment)
            member.save()
            return JsonResponse({'code': 200, 'form': [name, phone, comment, depatid]})
        else:
            return JsonResponse({'code': 100, 'msg': '数据效验失败'})


class MacView(View):
    # @csrf_exempt
    def get(self, request, *args, **kwargs):
        mmb_id = kwargs["mmb_id"]
        macs_obj = MacAddr.objects.filter(member_id=mmb_id)
        if macs_obj:
            data = []
            for mac in macs_obj:
                # print(mac.get_mactype_display()) 获取字面值
                tmpmac = model_to_dict(mac)
                tmpmac['mactype'] = mac.get_mactype_display()
                data.append(tmpmac)
            rspdata = {'code': 0, "count": len(macs_obj), "msg": "请求成功", 'data': data}
            return JsonResponse(rspdata)
        else:
            return JsonResponse({'code': 1, "count": 0, "msg": "该用户下没有mac记录"})

    def post(self, request, *args, **kwargs):
        pass


@login_required
def index(request):
    departs = []
    for depart_leve in (1, 2, 3):
        departs_obj = Department.objects.filter(level=depart_leve)
        departs.append(departs_obj)
    return render_to_response('index.html', {"content": departs})


def departmanage(request):
    return render(request, 'departdetails.html')


def dptpages(request):
    dptid = request.GET.get('dptid')
    limit = request.GET.get('pageSize')
    page = request.GET.get('pageIndex')
    print(dptid, limit, page)
    dpt = Department.objects.get(id=dptid)
    # dptmembers = Member.objects.filter(depart=Department_id)
    dptmembers = dpt.depart.all()
    paginator = Paginator(dptmembers, limit)
    pnpage = paginator.get_page(page)
    data = []
    for mem_ojb in pnpage.object_list:
        data.append(model_to_dict(mem_ojb))
    rsp = {'total': paginator.count, 'code': 0, 'msg': '请求成功',
           'page': page, 'limit': limit, 'data': data}
    return JsonResponse(rsp, json_dumps_params={'ensure_ascii': False})



def delmember(request, mmb_id):
    # member_id = kwargs["mmb_id"] form = PersonalMac()
    print('[post data] :', mmb_id)
    try:
        member_obj = Member.objects.get(id=mmb_id)
        member_obj.delete()
        rspdata = {'code': 0, 'msg': "删除成功", "status": 800}
        return JsonResponse(rspdata)
    except ObjectDoesNotExist:
        return JsonResponse({'code': 1, 'msg': "请求数据不存在！，请检查系统！", "status": 801})


def updatemember(request, mmb_id):
    form = MemberForm()
    if request.method == "GET":
        member = Member.objects.get(id=mmb_id)
        form.fields['name'].initial = member.name
        form.fields['phone'].initial = member.phone
        form.fields['comment'].initial = member.comment
        form.fields['departid'].initial = member._get_pk_val
        return render(request, "member_update.html", {'form': form, 'member': mmb_id})
    elif request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            comment = form.cleaned_data['comment']
            member = Member.objects.get(id=mmb_id)
            member.name = name
            member.phone = phone
            member.comment = comment
            member.save()
            print('post data', name)
            return JsonResponse({'code': 0, 'msg': "修改成功"})
    rspdata = {'code': 0, 'msg': "删除成功"}
    return JsonResponse(rspdata)


def addmac(request, mmb_id):
    # member_id = kwargs["mmb_id"]
    form = PersonalMac()
    if request.method == "POST":
        print('post data', mmb_id)
        form = PersonalMac(request.POST)
        if form.is_valid():
            mactype = form.cleaned_data['mactype']
            phaddr = form.cleaned_data['phaddr']
            comment = form.cleaned_data['comment']
            fw_mac = macconvert(phaddr)
            member = Member.objects.get(id=mmb_id)
            mac_ins = MacAddr(member=member, mactype=mactype, physic_mac=phaddr, fw_mac=fw_mac, comment=comment)
            mac_ins.save()
            return JsonResponse({'code': 0, 'msg': '添加成功'})
    return render(request, 'mac_add.html', {'form': form})


def login(request):
    if request.method == "POST":
        next_to = request.POST.get('next', False)
        loginForm = Login(request.POST)
        if loginForm.is_valid():
            name = loginForm.cleaned_data['name']
            passwd = loginForm.cleaned_data['passwd']
            try:
                user = User.objects.get(Q(username=name)|Q(email=name))
                if user.check_password(passwd):
                    auth.login(request, user)
                    return redirect('/')
            except ObjectDoesNotExist:
                render(request, 'login.html')
        elif next_to:
            return redirect(next_to)
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/login/')


def updatemac(request, mac_id):
    if request.method == "GET":
        # form.fields['mactype'].widget.choices = MACTYPE_CHOICES
        mac_obj = MacAddr.objects.get(id=mac_id)
        # form = PersonalMac(initial={'mactype': [mac_obj.mactype,], 'phaddr': mac_obj.physic_mac, 'comment':  mac_obj.comment})
        form = PersonalMac()
        form.fields['mactype'].initial = [ mac_obj.mactype, ]
        form.fields['phaddr'].initial = mac_obj.physic_mac
        form.fields['comment'].initial = mac_obj.comment
        return render(request, "mac_update.html", {'form': form, 'mac_id': mac_id})
    elif request.method == "POST":
        form = PersonalMac(request.POST)
        if form.is_valid():
            mactype = form.cleaned_data["mactype"]
            phaddr = form.cleaned_data["phaddr"]
            comment = form.cleaned_data["comment"]
            mac_obj = MacAddr.objects.get(id=mac_id)
            mac_obj.mactype = mactype
            mac_obj.physic_mac = phaddr
            mac_obj.comment = comment
            mac_obj.fw_mac = macconvert(phaddr)
            mac_obj.save();
            return JsonResponse({'code': 0, 'msg': "修改成功！", "status": 600})
        else:
            return JsonResponse({'code': 1, 'msg': "修改失败！，请检查系统！", "status": 601})



    elif request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            comment = form.cleaned_data['comment']
            member = Member.objects.get(id=mmb_id)
            member.name = name
            member.phone = phone
            member.comment = comment
            member.save()
            return JsonResponse({'code': 0, 'msg': "修改成功"})





def delmac(request, mac_id):
    print(mac_id)
    try:
        mac_obj = MacAddr.objects.get(id=mac_id)
        mac_obj.delete();
        return JsonResponse({'code': 0, 'msg': "删除成功！", "status": 600})
    except ObjectDoesNotExist:
        return JsonResponse({'code': 1, 'msg': "请求数据不存在！，请检查系统！", "status": 601})





def macconvert(physicmac):
    physicmac = physicmac.replace(":", "")
    fragment = [physicmac[0:4], physicmac[4:8], physicmac[8:]]
    fw_mac = "-".join(fragment)
    return fw_mac


def test(requset):
    print("entry test page!")
    return render(requset, 'test2.html')


def jsonrsp(requset):
    """
        如果是字典格式可以直接使用JsonResponse
        如果是列表格式，使用JsonResponse，需要添加safe=False
        使用JsonResponse都需要添加 json_dumps_params={'ensure_ascii':False} 否则显示不是UTF-8格式
    """
    dd = {'name': '朱昌辉', 'age': 30, 'addr': 'this is josn', 'rows': 5}
    return JsonResponse(dd)


def jsondata(requset):
    """
        如果是字典格式可以直接使用JsonResponse
        如果是列表格式，使用JsonResponse，需要添加safe=False
        使用JsonResponse都需要添加 json_dumps_params={'ensure_ascii':False} 否则显示不是UTF-8格式
    """
    # dd={'name': '朱昌辉', 'age': 30, 'addr': 'this is josn'}
    rsp = {"code": 0, 'msg': "查找成功", "count": 20, 'rows': 5, 'data': [{'name': 'pig'}, {'name': 'dog'}, {'name': 'cat'}]}

    return JsonResponse(rsp)
