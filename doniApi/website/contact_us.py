from doniApi.apiImports import Response, GenericAPIView, APIView, status
from doniServer.models import ContactUs, BpBasic
from rest_framework.permissions import IsAuthenticated, AllowAny


def contact_us_from_website(website_url, name, email, subject, message):
    business = BpBasic.get_business_using_website(website_url)
    contact_us = ContactUs(name=name, email=email, message=message, subject=subject)
    contact_us.business = business
    contact_us.save()



class ContactUsAPI(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        data = request.data
        base_url_2 = 'donigroup.com'
        contact_us_from_website(base_url_2, data.get('name'), data.get('email'), \
                                data.get('subject'), data.get('comments'))

        return Response({'success': True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        print 'hello--------------------------------------'
        return Response({'success': True}, status=status.HTTP_200_OK)
