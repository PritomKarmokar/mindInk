from django.contrib import admin

from accounts.models import User, PasswordReset

admin.site.register(User)

admin.site.register(PasswordReset)
