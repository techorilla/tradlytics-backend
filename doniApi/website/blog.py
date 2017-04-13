from doniApi.apiImports import Response, GenericAPIView, APIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from website.models import *
from doniCore.utils import Utilities
import os, json
from datetime import datetime as dt
import traceback
import sys
from django.utils.safestring import mark_safe


class BlogTagAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        filter_tags = Tag.objects.filter(name__icontains=query).values('name').order_by('name')
        filter_tags = [tag.get('name') for tag in filter_tags]
        return Response(filter_tags, status=status.HTTP_200_OK)


class BlogDisplayAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            base_url = request.META.get('HTTP_HOST')
            data = request.data
            research_id = data.get('researchId')
            research = Post.objects.get(id=research_id)
            if research.display_on_web:
                message = 'Research now being displayed on website'
            else:
                message = 'Research removed from displayed on website'
            research.display_on_web = not research.display_on_web
            research.save()
            return Response({
                'researchObj': research.get_list_obj(base_url, request.user),
                'success': True,
                'message': message
            }, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })


class BlogAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    messages = dict()
    messages['successPOST'] = 'Research Blog created successfully.'
    messages['successPUT'] = 'Research Blog updated successfully.'

    def make_new_research_tags(self, research_tags):
        tag_exist = Tag.objects.filter(name__in=research_tags).values('name')

        tag_exist = [tag.get('name') for tag in tag_exist]
        new_tags = [tag for tag in research_tags if tag not in tag_exist]
        for n_tag in new_tags:
            tag = Tag()
            tag.name = n_tag
            tag.save()

    def save_blog(self, request):
        try:
            base_url = request.META.get('HTTP_HOST')
            research_image = request.FILES.get('image')
            research_data = json.loads(request.data.get('research'))
            research_id = research_data.get('id')
            research_draft = research_data.get('isDraft')
            research_title = research_data.get('title')
            research_slug = research_data.get('slug')
            research_tags = research_data.get('tags')
            research_tags = [tag.get('text') for tag in research_tags]
            self.make_new_research_tags(research_tags)
            height = research_data.get('height')
            width = research_data.get('width')
            research_content = research_data.get('content')
            if research_id:
                success_message = self.messages['successPUT']
                research = Post.objects.get(id=research_id)
                research.updated = dt.now()
                if research.image and research_image:
                    path = Utilities.get_media_directory() + '/' + str(research.image)
                    os.remove(path)
            else:
                research = Post()
                success_message = self.messages['successPOST']
            research.image = research_image
            research.slug = research_slug
            research.user = request.user
            research.title = research_title
            research.height_field = height
            research.width_field = width
            research.content = research_content
            research.draft = research_draft
            if not research_draft:
                research.publish = dt.now()
            else:
                research.publish = None
            tags = Tag.objects.filter(name__in=research_tags)
            research.save()
            for tag in tags:
                research.tags.add(tag)
            research.save()
            return Response({
                'success':True,
                'researchObj': research.get_list_obj(base_url, request.user),
                'message': success_message
            })
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })

    def post(self, request, *args, **kwargs):
        return self.save_blog(request)

    def put(self,  request, *args, **kwargs):
        return self.save_blog(request)

    def delete(self, request, *args, **kwargs):
        success = False
        try:
            user = request.user
            research_id = kwargs.get('research_id')
            research = Post.objects.get(id=research_id)
            if research.image:
                path = Utilities.get_media_directory() + '/' + str(research.image)
                os.remove(path)

            if (research.user == user) or user.is_superuser:
                research.delete()
                success = True
                message = 'Research has been delete successfully';
            else:

                message = 'You are not authorized to delete this researh'
        except Exception, e:
            message = str(e)
            success = False

        return Response({
            'success': success,
            'message': message
        })

    def get(self, request, *args, **kwargs):
        research_id = request.GET.get('researchId')
        base_url = request.META.get('HTTP_HOST')
        if research_id:
            research = Post.objects.get(id=research_id)
            return Response({'researchObj': research.get_complete_obj(base_url)}, status=status.HTTP_200_OK)
        else:
            blogs = Post.objects.all()
            blogs = [blog.get_list_obj(base_url, request.user) for blog in blogs]
            return Response({'researchList': blogs, 'success': True}, status=status.HTTP_200_OK)