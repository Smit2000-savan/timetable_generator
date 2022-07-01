from django.contrib import admin

# Register your models here.
from .models import Prof, Course, Batch, Available, C_pref, Time_to_slot, P_pref, Slots

admin.site.register(Prof)
admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(Available)
admin.site.register(C_pref)
admin.site.register(Time_to_slot)
admin.site.register(P_pref)
admin.site.register(Slots)