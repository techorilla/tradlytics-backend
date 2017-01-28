
from rest_framework import serializers
from doniServer.models import Blog
from .tag import TagSerializer


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.Field(source='author.username')
    tags_details = TagSerializer(source='tags', read_only=True)
    api_url = serializers.SerializerMethodField('get_api_url')

    class Meta:
        model = Blog
        fields = ('id', 'title', 'description', 'created_on', 'author', 'tags',
                  'tags_details', 'url', 'api_url')
        read_only_fields = ('id', 'created_on')

    def get_api_url(self, obj):
        return "#/post/%s" % obj.id