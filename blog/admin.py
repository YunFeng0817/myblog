from django.contrib import admin
from blog import models
# Register your models here.
class blogsAdmin(admin.ModelAdmin):
    list_display = ('title','introduction','author','writeDate')
class photoAdmin(admin.ModelAdmin):
    list_display = ('author','introduction')
admin.site.register(models.diary,blogsAdmin)
admin.site.register(models.tech,blogsAdmin)
admin.site.register(models.trip,blogsAdmin)
admin.site.register(models.photo,photoAdmin)
admin.site.register(models.comment)
admin.site.register(models.image)
admin.site.register(models.file)
admin.site.register(models.label)