from django.contrib import admin
from blog import models
# Register your models here.
class blogsAdmin(admin.ModelAdmin):
    list_display = ('title','content','author','writDate')
admin.site.register(models.storge,blogsAdmin)