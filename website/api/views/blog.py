from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from doniApi.apiImports import Response, GenericAPIView, status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from website.models import Post, Tag
from django.utils import timezone

from website.serializers.single_blog import SingleBlogSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )


class BlogPage(View):
    template_name = 'blog.html'

    def get(self, request, *args, **kwargs):
        tags = Tag.objects.filter(blog__isnull=False).values('name', 'slug').distinct()
        today = timezone.now().date()
        queryset_list = Post.objects.active().order_by("-timestamp")


        query = request.GET.get("q")
        tag = request.GET.get("tag")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        if tag:
            query_tag = Tag.objects.filter(name=tag)
            queryset_list = Post.objects.filter(tags__in=query_tag).distinct()
        paginator = Paginator(queryset_list, 8)  # Show 25 contacts per page
        page_request_var = "page"
        page = request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        context = {

            "tags": tags,
            "object_list": queryset,
            "title": "List",
            "page_request_var": page_request_var,
            "today": today,
        }
        return render(request, self.template_name, context)


import urllib


class SingleBlog(View):
    template_name = 'post.html'

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        instance = get_object_or_404(Post, slug=slug)
        if instance.publish > timezone.now().date() or instance.draft:
            if not request.user.is_staff or not request.user.is_superuser:
                raise Http404

        tags = Tag.objects.filter(blog__isnull=False).values('name', 'slug').distinct()
        instance.increment_visitor()

        context = {
            "tags": tags,
            "title": instance.title,
            "instance": instance,
            "share_string": urllib.pathname2url(instance.content),
        }
        return render(request, self.template_name, context)



