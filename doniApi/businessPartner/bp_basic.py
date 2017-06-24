from doniApi.apiImports import Response, GenericAPIView, status
from doniCore.utils import Utilities
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import BpBasic, BusinessType
import json, os
from datetime import datetime as dt
from doniCore import cache_results
from doniCore.cache import cache, doni_redis
from django.conf import settings



class BusinessListAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    @cache_results
    def get_business_list(self, business, base_url, alpha='A'):
        all_business_query = BpBasic.objects.filter(created_by__profile__business=business)
        all_business = all_business_query.filter(bp_name__startswith=alpha).order_by('bp_name').exclude(bp_id=business.bp_id)
        all_business = map(lambda business: business.get_list_obj(base_url), all_business)
        all_business_count = all_business_query.count()
        return {
            'list':all_business,
            'count':all_business_count
        }

    def get(self, request, *args, **kwargs):
        user = request.user
        alpha = request.GET.get('alpha')
        base_url = request.META.get('HTTP_HOST')
        business = Utilities.get_user_business(user)
        all_business = self.get_business_list(business, base_url, alpha)
        return Response({'businessList': all_business}, status=status.HTTP_200_OK)



class BpBasicAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    messages = dict()
    cache_methods = ['get_business_list']
    messages['errorPOST'] = 'Business was not created due to some error on server.'
    messages['successPOST'] = 'Business created successfully.'
    messages['successPUT'] = 'Business basic information updated successfully.'
    messages['errorPUT'] = 'Business was not updated due to some error on server.'

    def get(self, request, *args, **kwargs):
        bp_id = request.GET.get('bpId')
        business = BpBasic.objects.get(bp_id=bp_id)
        base_url = request.META.get('HTTP_HOST')
        return Response({'business': business.get_obj(base_url)})

    def delete_cache(self, business, base_url):
        for method in self.cache_methods:
             key_str = list()
             key_str.append(method)
             key_str.append(business.__unicode__())
             key_str.append(settings.APP_DOMAIN)
             key = '_'.join(key_str)
             cache.delete(key)
             print 'deleting cache key %s'%key

        cache.delete('get_all_business_drop_down_Seller')
        print 'Cache key: get_all_business_drop_down_Seller'
        cache.delete('get_all_business_drop_down_Buyer')
        print 'Cache key: get_all_business_drop_down_Buyer'


    def post(self, request, *args, **kwargs):
        try:
            logo = request.FILES.get('logo')
            business_data = request.data.get('data')
            business_data = json.loads(business_data)
            business_type = business_data.get('bpType')
            business_type = BusinessType.objects.filter(id__in=business_type)
            business = BpBasic()
            business.bp_logo = logo
            business.bp_name = business_data.get('name')
            business.bp_ntn = business_data.get('ntn')
            business.bp_website = business_data.get('website')
            business.bp_database_id = business_data.get('databaseId')
            business.created_by = request.user
            business.save()
            for type in business_type:
                business.bp_types.add(type)
            business.save()
            base_url = request.META.get('HTTP_HOST')
            user_business = request.user.profile.business
            self.delete_cache(user_business, base_url)
            return Response({
                'success': True,
                'bpId': business.bp_id,
                'message': self.messages['successPOST']
            }, status=status.HTTP_200_OK)
        except Exception, e:
            print str(e)
            return Response({
                'success': False,
                'message': self.messages['errorPOST']
            })

    def put(self, request, *args, **kwargs):
        try:

            logo = request.FILES.get('logo')
            print logo
            business_data = request.data.get('data')
            business_data = json.loads(business_data)
            business_id = business_data.get('bpId')
            business_type_id = business_data.get('bpType')
            business = BpBasic.objects.get(bp_id=business_id)
            if business.bp_logo and logo:
                path = Utilities.get_media_directory()+'/'+str(business.bp_logo)
                os.remove(path)
                business.bp_logo = logo
            business.bp_name = business_data.get('name')
            business.bp_ntn = business_data.get('ntn')
            business.bp_website = business_data.get('website')
            business.updated_by = request.user
            business.bp_logo = logo
            business.updated_at = dt.now()
            business.save()

            business_type_removed = business.bp_types.exclude(id__in=business_type_id)
            business_types = BusinessType.objects.filter(id__in=business_type_id)

            # Removing Business Types
            for type in business_type_removed:
                business.bp_types.remove(type)
            # Adding Business Types
            for type in business_types:
                if not business.bp_types.filter(id=type.id).exists():
                    business.bp_types.add(type)
            business.save()
            base_url = request.META.get('HTTP_HOST')
            user_business = request.user.profile.business
            self.delete_cache(user_business, base_url)
            return Response({
                'success': True,
                'bpId': business.bp_id,
                'message': self.messages['successPUT']
            })
        except Exception, e:
            print e
            return Response({
                'success': False,
                'message': self.messages['errorPUT']
            })

    def delete(self, request, *args, **kwargs):

        return Response()


