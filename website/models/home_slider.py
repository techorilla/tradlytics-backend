from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)
    HomeSliderModel = instance.__class__
    try:
        new_id = HomeSliderModel.objects.order_by("id").last().id + 1
    except AttributeError:
        new_id = 1
    return os.path.join('home_slider', str(new_id), filename)


class HomeSlider(models.Model):
    image = models.ImageField(upload_to=upload_location)
    heading = models.TextField()
    sub_heading = models.TextField()
    call_to_action_text = models.CharField(max_length=200, default=None, null=True)
    call_to_action_url = models.CharField(max_length=200, default=None, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='slider_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='slider_updated_by')

    def __unicode__(self):
        return self.heading

    def __str__(self):
        return self.heading


from django.contrib import admin


class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ('heading', 'sub_heading', 'created_by')
    exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()
        return obj

