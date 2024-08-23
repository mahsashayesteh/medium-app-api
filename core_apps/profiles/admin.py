from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['pkid', 'id', 'user', 'gender', 'phonenumber', 'country',
                    'city']
    list_filter = ['pkid', 'id', 'user', 'phonenumber']
    list_display_links = ['pkid', 'id', 'user']

admin.site.register(Profile, ProfileAdmin)
