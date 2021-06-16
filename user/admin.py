from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .forms import UserMyCreationForm, UserMyChangeForm
from .models import User


class UserMyAdmin(UserAdmin):
    add_form = UserMyCreationForm
    form = UserMyChangeForm
    model = User
    list_display = ('email', 'address',)
    list_filter = ('email', 'address',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'address',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserMyAdmin)
