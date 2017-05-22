from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib import admin


class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='prod_category_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='prod_category_updated_by')

    @classmethod
    def get_category_for_website(cls):
        categories = cls.objects.filter(products__on_website=True).distinct()
        return [cat.get_category_list() for cat in categories]

    @property
    def category_class(self):
        return '_'.join(self.name.lower().split(' '))

    @property
    def keyword_count(self):
        keyword_count = self.keywords.all().count()
        return int(keyword_count)

    @property
    def product_count(self):
        product_count = self.products.all().count()
        return int(product_count)

    @classmethod
    def get_category_drop_down(cls):
        all_cat = cls.objects.all()
        return [{
            'id': cat.id,
            'name': cat.name
        } for cat in all_cat]

    def get_obj(self):
        return {
            'id': self.id,
            'name': self.name,
            'productCount': self.product_count,
            'keywordCount': self.keyword_count,
            'description': self.description
        }

    def get_category_list(self):
        return {
            'name': self.name,
            'products': self.product_count,
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
