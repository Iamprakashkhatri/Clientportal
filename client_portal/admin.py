from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Project,Member,CommentsGroups,Comments,Reply
from guardian.admin import GuardedModelAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Member)
admin.site.register(CommentsGroups)
admin.site.register(Reply)
admin.site.register(Comments)

class ProjectAdmin(GuardedModelAdmin):
    # prepopulated_fields = {"name": ("title",)}
    list_display = ('title', 'type')
    search_fields = ('name', 'address')

admin.site.register(Project, ProjectAdmin)
