from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile

# Register your models here.

admin.site.site_title = "Admin Panel"
admin.site.site_header = "RGPI MCC Administrator"
admin.site.index_title = "Site Administrator"

admin.site.register(Profile)