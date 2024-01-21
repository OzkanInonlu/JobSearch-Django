from django.contrib import admin
from .models import *
from users.models import *
from django.contrib.auth import get_user_model

# Register your models here.

User = get_user_model()
class ResumeAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name", "created_at"]
    list_filter = ["user"]
    search_fields = ["user__username", "user__email"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "email"]
    list_filter = ["user", "email"]
    search_fields = ["user__username", "email"]

admin.site.register(Resume, ResumeAdmin)
admin.site.register(Company)
admin.site.register(JobAdvert)
admin.site.register(User)
admin.site.register(ApplyJob)
admin.site.register(Industry)
admin.site.register(Comment, CommentAdmin)
