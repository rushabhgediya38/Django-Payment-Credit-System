from django.contrib import admin
from .models import Post, Comment, Credit, StartupSubmissionList
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class StartupSubmissionListResource(resources.ModelResource):
    class Meta:
        model = StartupSubmissionList
        exclude = ('user',)


class StartupSubmissionListAdmin(ImportExportModelAdmin):
    resource_class = StartupSubmissionListResource

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Credit)
admin.site.register(StartupSubmissionList, StartupSubmissionListAdmin)
# admin.site.register(SSListUser)

