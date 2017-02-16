from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone


class ProductKeyword(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=100, blank=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='keyword_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='keyword_updated_by')

    def __unicode__(self):
        return self.keyword

    class Meta:
        db_table = 'product_keywords'
        ordering = ('keyword',)


from django.contrib import admin


class ProductKeywordAdmin(admin.ModelAdmin):
    model = ProductKeyword
    list_display = ('keyword', 'created_by', 'created_at')
    fieldsets = [
        ('Category Details', {'fields': ['keyword']})
    ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

