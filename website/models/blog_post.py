from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from .blog_comment import Comment
from .blog_tag import Tag
import os
from ..utitlities import get_read_time
import time

# Create your models here.
# MVC MODEL VIEW CONTROLLER


# Post.objects.all()
# Post.objects.create(user=user, title="Some time")

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False, display_on_web=True).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)
    PostModel = instance.__class__
    try:
        new_id = PostModel.objects.order_by("id").last().id + 1
    except AttributeError:
        new_id = 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    print filename, new_id
    return os.path.join('blogs', str(new_id), str(time.time())+'_'+filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    tags = models.ManyToManyField(Tag, related_name='blog')
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    display_on_web = models.BooleanField(default=False)
    visitors = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False, default=None, null=True)
    read_time = models.IntegerField(default=0)  # models.TimeField(null=True, blank=True) #assume minutes
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def increment_visitor(self):
        self.visitors += 1
        self.save()

    @property
    def safe_content(self):
        return mark_safe(self.content)

    def get_complete_obj(self, base_url):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'tags': [tag.name for tag in self.all_tags],
            'image': self.get_blog_image(base_url),
            'height': self.height_field,
            'width': self.width_field,
            'content': self.content
        }

    def get_absolute_url(self):
        return reverse("web:detail", kwargs={"slug": self.slug})

    def get_api_url(self):
        return reverse("web:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_list_obj(self, base_url, user):
        return {
            'id': self.id,
            'visitors': self.visitors,
            'canEdit': (self.user == user),
            'displayOnWeb': self.display_on_web,
            'canDelete': (self.user == user) or user.is_superuser,
            'createdByImage': self.user.profile.get_profile_pic(base_url),
            'createdBy': self.user.username,
            'createdOn': self.timestamp,
            'title': self.title,
            'image': str(self.get_blog_image(base_url)),
            'comments': self.comments.count(),
            'isDraft': self.draft,
            'reads': self.read_time,
            'publishedOn': self.publish,
            'tags': [{
                'id': tag.id,
                'name': tag.name
            } for tag in self.all_tags]
        }

    def get_blog_image(self, base_url):
        pre = 'https://' if settings.IS_HTTPS else 'http://'
        return pre + base_url + '/media/' + str(self.image) if self.image else None

    @property
    def get_markdown(self):
        try:
            content = self.content
            markdown_text = markdown(content)
            return mark_safe(markdown_text)
        except Exception, e:
            print str(e)
            return None


    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def all_tags(self):
        instance = self
        tgs = instance.tags.all()
        return tgs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.content
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender=Post)










