from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('email', 'name', 'last_name', 'is_staff', 'is_active')
    list_filter = (
        ('is_staff', admin.BooleanFieldListFilter),
    )

