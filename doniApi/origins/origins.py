from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import Origin
from rest_framework.permissions import IsAuthenticated, AllowAny


class OriginsAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        origin_id = kwargs.get('origin_id')
        if origin_id is None:
            all_origins = Origin.objects.all()
            all_origins = [{
                'id': org.id,
                'name': org.name
            } for org in all_origins]
            return Response({'origins': all_origins}, status.HTTP_200_OK)
        else:
            origin = Origin.objects.get(id=int(origin_id))
            return Response({
                'id': origin.id,
                'name': origin.name}, status=status.HTTP_200_OK)

    def origin_already_exist(self, name):
        origin = Origin.objects.filter(name=name)
        if len(origin) == 0:
            return False
        else:
            return True

    def post(self, request, *args, **kwargs):
        origin_data = request.data
        name = origin_data.get('name')
        if not self.origin_already_exist(name):
            user = request.user
            origin = Origin(name=name)
            origin.created_by = user
            origin.save()
            return Response({'id': origin.id}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_409_CONFLICT)

    def delete(self, request, *args, **kwargs):
        origin_id = kwargs.get('origin_id')
        origin = Origin.objects.get(id=origin_id)
        origin.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        origin_id = kwargs.get('origin_id')
        origin_data = request.data
        user = request.user
        origin = Origin.objects.get(id=origin_id)
        origin.name = origin_data.get('name')
        origin.updated_by = user
        origin.save()
        return Response(status=status.HTTP_200_OK)