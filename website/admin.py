from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import Comment
from .models import Post
from .models import Tag, TagModelAdmin
from .models import HomeSlider, HomeSliderAdmin, HomeServices, HomeServicesAdmin


admin.site.register(Comment)
admin.site.register(Tag, TagModelAdmin)
admin.site.register(HomeSlider, HomeSliderAdmin)
admin.site.register(HomeServices, HomeServicesAdmin)


