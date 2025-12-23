from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department', 'hired_at', 'salary')
    list_filter = ('department', 'hired_at')
    search_fields = ('full_name', 'position')
    list_select_related = ('department',)
    ordering = ('full_name',)
