from django.contrib import admin
from backend import models

# Register your models here.

class UsernameAdmin(admin.ModelAdmin):
    list_display = ('username','sex', 'age', 'education', 'research')

class DurationAdmin(admin.ModelAdmin):
    list_display = ('did', 'time', 'name', 'consumingtime', 'username')

class RectangleAdmin(admin.ModelAdmin):
    list_display = ('rid', 'time', 'name', 'x1', 'y1', 'x2', 'y2', 'username', 'duration')

admin.site.register(models.Username, UsernameAdmin)
admin.site.register(models.Duration, DurationAdmin)
admin.site.register(models.Rectangle, RectangleAdmin)
