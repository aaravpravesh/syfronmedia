from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Assignment, Contact

class UserAdmin(BaseUserAdmin):
    # Columns to display in list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    # Field layout in edit form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "subject", "message")
    ordering = ("-created_at",)
    readonly_fields = ("name", "email", "subject", "message", "created_at")


# Unregister default User admin and register our customized one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Assignment)
