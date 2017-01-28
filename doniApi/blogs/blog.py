from rest_framework import generics
from rest_framework import permissions
from doniServer.models.blogs import Blog
from doniServer.serializers import BlogSerializer
from doniServer.permissions import IsOwnerOrReadOnly


class BlogList(generics.ListCreateAPIView):
    """
    List all boards, or create a new board.
    """
    model = Blog
    serializer_class = BlogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.author = self.request.user


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a board instance.
    """
    model = Blog
    serializer_class = BlogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
