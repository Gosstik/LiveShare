from django.contrib import admin

from users.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = ("id",) + self.list_display


admin.site.register(User, UserAdmin)
