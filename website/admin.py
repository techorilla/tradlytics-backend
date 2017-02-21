from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import Comment
from .models import Post, PostModelAdmin
from .models import Tag, TagModelAdmin
from .models import HomeSlider, HomeSliderAdmin


admin.site.register(Comment)
admin.site.register(Post, PostModelAdmin)
admin.site.register(Tag, TagModelAdmin)
admin.site.register(HomeSlider, HomeSliderAdmin)
