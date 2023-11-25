from django.contrib import admin
from users.models import User
from users.models import Permission
from users.models import Role
# Register your models here.

admin.site.register(User)
admin.site.register(Permission)
admin.site.register(Role)
