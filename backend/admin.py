from django.contrib import admin
from .models import Zaplecze, Account
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class ZapleczeAdmin(admin.ModelAdmin):
    list_display = ['domain', 'email', 'url', 'login', 'password', 'topic']


admin.site.register(Zaplecze, ZapleczeAdmin)



class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class CustomUserAdmin(UserAdmin):
    inlines = (AccountInline, )

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'tokens_used', 'openai_api_key', 'semstorm_api_key')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# admin.site.register(Account)
admin.site.register(Account, AccountAdmin)