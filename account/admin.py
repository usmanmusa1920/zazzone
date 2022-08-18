from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Profile, FriendRequest
from board.models import Board

User = get_user_model()


class ProfileInline(admin.TabularInline):
  model = Profile
  extra = 1
  
  
  
class BoardInline(admin.TabularInline):
  model = Board
  extra = 1
  
  
  
class UserAdminForm(UserAdmin):
  search_fields = ('username', 'phone_number', 'email',)
  ordering = ('-date_joined',)
  list_filter = ('first_name', 'last_name', 'gender', 'date_of_birth', 'username', 'email', 'phone_number', 'country', 'image', 'is_active', 'is_verified','is_superuser', 'is_staff', 'is_admin')
  list_display = ('first_name', 'last_name', 'gender', 'last_login', 'date_of_birth', 'username', 'email', 'phone_number', 'country', 'image', 'is_active', 'is_verified','is_superuser', 'is_staff', 'is_admin')
  
  # These are the field that will display when you want to edit user account via admin
  fieldsets = (
      (None , {"fields": ('password', 'username', 'phone_number', 'email',)}),
      ('Permissions', {"fields": ('is_active', 'is_verified','is_superuser', 'is_staff', 'is_admin', 'is_num_encrypt', 'is_email_encrypt', 'is_dob_encrypt',)}),
      ('Personal', {"fields": ('image', 'first_name', 'last_name', 'gender', 'date_of_birth', 'country','friends',)}),
      ('Account activity', {"fields": ('last_login', 'date_joined',)}),
  )
  
  # These are the field that will display when you want to create new user account via admin
  add_fieldsets = (
    (None, {
      'classes':('wide',),
      'fields':('first_name', 'last_name', 'gender', 'date_of_birth', 'username', 'email', 'phone_number', 'country', 'friends', 'image', 'is_active', 'is_verified','is_superuser', 'is_staff', 'is_admin', 'password1', 'password2')
    }),
  )
  
  inlines = [ProfileInline, BoardInline]
  filter_horizontal = ()
  
  
admin.site.site_header = 'Zazzone'
admin.site.site_title = 'Zazzone'
admin.site.index_title = 'Zazzone admin'

admin.site.unregister(Group)

admin.site.register(User,UserAdminForm)
admin.site.register(Profile)
admin.site.register(FriendRequest)