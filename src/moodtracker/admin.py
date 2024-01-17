from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin

from patient.models import CustomUser


class MyAdminSite(AdminSite):

    def get_urls(self):
        urls = super(MyAdminSite, self).get_urls()
        return urls


admin_site = MyAdminSite()


@admin.register(CustomUser, site=admin_site)
class CustomUserAdmin(UserAdmin):
    # we want non-superusers by default
    def get_queryset(self, request):
        return CustomUser.objects.filter(patient__isnull=True, is_superuser=False)

    list_display = ("username", "email", "first_name", "last_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("username", "first_name", "last_name", "email")
