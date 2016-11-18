from django.contrib import admin

from .models import Member
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (MemberInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
