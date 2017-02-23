from django.contrib import admin

# Register your models here.
from .models import EmailBase, EmailBaseAdmin
from .models import EmailMessage, EmailMessageAdmin

admin.site.register(EmailBase, EmailBaseAdmin)
admin.site.register(EmailMessage, EmailMessageAdmin)