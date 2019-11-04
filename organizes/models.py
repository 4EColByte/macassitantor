from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(max_length=11, verbose_name='手机号',  null=True,)
    nickname = models.CharField(max_length=30, verbose_name="昵称")

    class Meta:
        db_table = 'userex'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return {'name': self.username, 'nickname': self.nickname}


class Department(models.Model):
    level_choices = ((1, "一级部门"), (2, "一级部门"))
    id = models.AutoField('id', primary_key=True)
    name = models.CharField(max_length=40)
    level = models.SmallIntegerField(choices=level_choices, default=-1)
    parent = models.SmallIntegerField(null=True)
    comments = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "department"
        verbose_name = "部门"


class Member(models.Model):
    stats_choice = ((True, '在职'), (False, '离职'), )
    id = models.AutoField('ID', primary_key=True)
    name = models.CharField(max_length=40)
    phone = models.CharField(max_length=11)
    depart = models.ForeignKey(Department, related_name='depart', on_delete=models.DO_NOTHING)
    stats = models.BooleanField(choices=stats_choice, default=True)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "member"
        verbose_name = "员工"

MACTYPE_CHOICES = (
  (1, '有线'),
  (2, '无线'),
  (3, '其他'),
)
class MacAddr(models.Model):
    id = models.AutoField('id', primary_key=True)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    mactype = models.IntegerField(choices=MACTYPE_CHOICES)
    physic_mac = models.CharField(max_length=17)
    fw_mac = models.CharField(max_length=16)
    comment = models.CharField(max_length=200)

    class Meta:
        db_table = "macs"
        verbose_name = "mac地址"

    def __str__(self):
        return self.comment
