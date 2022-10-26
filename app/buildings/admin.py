from django.contrib import admin
from buildings.models import Building


@admin.register(Building)
class UserAdmin(admin.ModelAdmin):
    ordering = ('year',)
    list_display = ('name', 'year',
                    'quarter', 'builder')
    search_fields = ('quarter', 'builder', 'year')
