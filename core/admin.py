from django.contrib import admin
from core.models import User,Profile,Message

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'full_name']

admin.site.register(User, UserAdmin)
# admin.site.register( Profile,ProfileAdmin)
admin.site.register(Message)
admin.site.register(Profile)
