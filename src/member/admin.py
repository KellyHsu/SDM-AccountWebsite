from django.contrib import admin

from .models import Member
from account.models import Receipt
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class ReceiptInline(admin.StackedInline):
    model = Receipt


class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    inlines = (ReceiptInline, )


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (MemberInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
