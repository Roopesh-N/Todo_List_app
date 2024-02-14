from django.contrib import admin
from todoApp.models import userModel,task
# Register your models here.

class userModelAdmin(admin.ModelAdmin):
    list_display=['firstname','lastname','username','password','phone','email']
    prepopulated_fields = {"slug": ("firstname", "lastname")}

admin.site.register(userModel,userModelAdmin)

class taskAdmin(admin.ModelAdmin):
    list_display=['user','title','description','date']

admin.site.register(task,taskAdmin)