from django.contrib import admin
from .models import Account

# Insert your models here To access them on admin page
class AccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(Account,AccountAdmin)
