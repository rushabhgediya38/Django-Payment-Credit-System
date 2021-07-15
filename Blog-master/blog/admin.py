from django.contrib import admin
from .models import Post, Comment, Credit, SSList

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Credit)
admin.site.register(SSList)
# admin.site.register(SSListUser)
