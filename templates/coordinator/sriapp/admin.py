from django.contrib import admin

# Register your models here.
from .models import Prof, Course, Batch, Available

admin.site.register(Prof)
admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(Available)