from django.contrib import admin
from .models import *



admin.site.register(User)
admin.site.register(BadData)
admin.site.register(BadWord)
admin.site.register(Comments)
admin.site.register(Group)