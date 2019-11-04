from django.contrib import admin
from .models import Member, MacAddr, Department


# Register your models here.
# admin.site.register([Member, Macaddr, Department])
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    fields = (('id', 'name'), 'phone')
