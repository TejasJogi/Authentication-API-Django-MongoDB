from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

class UserAdmin(BaseUserAdmin):
      # The fields to be used in displaying the User model.
  # These override the definitions on the base UserAdmin
  # that reference specific fields on auth.User.
  list_display = ('username', 'email', 'phone', 'is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('username', 'phone')}),
      ('Permissions', {'fields': ('is_admin',)}),
  )
  # add_fieldsets is not a standard Admin attribute. UserAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ( 'username', 'email', 'phone', 'password1', 'password2'),
      }),
  )
  search_fields = ('email',)
  ordering = ('email',)
  filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)