from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .productCategory import ProductCategory
from jsonfield import JSONField


class ProductsSpecification(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, null=True, default='Product Specification')
    specs = JSONField(null=True)
    productCategory = models.OneToOneField(
        ProductCategory,
        null=True,
        default=None,
    )
    # moisture = models.FloatField(default=None, null=True)
    # purity = models.FloatField(default=None, null=True)
    # weaveled = models.FloatField(default=None, null=True)
    # splits = models.FloatField(default=None, null=True)
    # damaged = models.FloatField(default=None, null=True)
    # foreignMatter = models.FloatField(default=None, null=True)
    # greenDamaged = models.FloatField(default=None, null=True)
    # otherColor = models.FloatField(default=None, null=True)
    # wrinkled = models.FloatField(default=None, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='specs_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='specs_updated_by')

    class Meta:
        db_table = 'product_specs'

    def __unicode__(self):
        return self.name


# from django.contrib import admin
# from jsoneditor.forms import JSONEditor


# class ProductsSpecificationAdmin(admin.ModelAdmin):
#     model = ProductsSpecification
#     formfield_overrides = {
#         JSONField: {'widget': JSONEditor},
#     }
#     fieldsets = [
#         ('Specification Details', {'fields': ['name', 'productCategory']}),
#         ('Specifications', {'fields': ['specs']})
#     ]
#
#     def save_model(self, request, obj, form, change):
#         obj.created_by = request.user
#         obj.save()





