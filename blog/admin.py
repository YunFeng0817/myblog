from django.contrib import admin
from blog import models
# Register your models here.
class blogerAdmin(admin.ModelAdmin):
    list_display = ('blogID','blogName', 'createTime')
class blogsAdmin(admin.ModelAdmin):
    list_display = ('title','content','author','writDate')
admin.site.register(models.blogger,blogerAdmin)
admin.site.register(models.blogs,blogsAdmin)