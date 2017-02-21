from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib import admin

class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='prod_category_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='prod_category_updated_by')

    @classmethod
    def get_category_for_website(cls):
        categories = cls.objects.all()
        return [cat.get_category_list() for cat in categories]

    @property
    def category_class(self):
        return '_'.join(self.name.lower().split(' '))

    @property
    def abc(self):
        return 'abc'

    def get_category_list(self):
        return {
            'name': self.name,
            'products': self.products.all(),
            'class': self.category_class,
            'count': str(self.products.all().count())
        }

    class Meta:
        db_table = 'product_category'

    def __unicode__(self):
        return self.name


class ProductsCategoryAdmin(admin.ModelAdmin):
    model = ProductCategory
    fieldsets = [
        ('Category Details', {'fields': ['name']})
    ]
    list_display = ('name', 'created_by', 'created_at')

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()
