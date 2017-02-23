from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from markdownx.models import MarkdownxField
import os


class EmailBase(models.Model):
    name = models.CharField(max_length=200, null=False)
    template = MarkdownxField()

    def __unicode__(self):
        return self.name


class EmailMessage(models.Model):
    name = models.CharField(max_length=200, null=False)
    base_template = models.ForeignKey(EmailBase, default=1)
    body = MarkdownxField()

    def __unicode__(self):
        return self.name



from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from markdownx.widgets import AdminMarkdownxWidget


class EmailBaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget}
    }



class EmailMessageAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


