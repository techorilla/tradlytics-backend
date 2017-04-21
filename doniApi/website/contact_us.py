from doniApi.apiImports import Response, GenericAPIView, APIView, status
from doniServer.models import ContactUs, BpBasic
from rest_framework.permissions import IsAuthenticated, AllowAny
from emailApp.email_manager import send_email
from doniGroup.authentication import CsrfExemptSessionAuthentication
from django.conf import settings


def contact_us_from_website(website_url, name, email, subject, message):
    business = BpBasic.get_business_using_website(website_url)
    contact_us = ContactUs(name=name, email=email, message=message, subject=subject)
    contact_us.business = business
    contact_us.save()


def validated_contact_us(name, email, subject, message):
    import re
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not EMAIL_REGEX.match(email):
        return Response({'success': False, 'message': 'Please Enter a valid email'})
    if name == '':
        return Response({'success': False, 'message': 'Please enter your name.'})
    if email == '':
        return Response({'success': False, 'message': 'Please enter your email.'})
    if subject == '':
        return Response({'success': False, 'message': 'Please enter a subject.'})
    if message == '':
        return Response({'success': False, 'message': 'Please enter a message'})
    return None




class ContactUsAPI(APIView):

    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        data = request.data
        base_url_2 = 'donigroup.com'
        contact_us_from_website(base_url_2, data.get('name'), data.get('email'), \
                                data.get('subject'), data.get('comments'))
        validated_error = validated_contact_us(data.get('name'), data.get('email'), \
                                data.get('subject'), data.get('comments'))

        if validated_error is None:
            send_email.delay('Contact Us',
                             {
                                 'name': data.get('name')
                             },
                             'Thanks for Contacting Doni & Company',
                             send_to_email= [data.get('email')])

            send_email.delay('Contact Us Recieved', {
                'name': data.get('name'),
                'subject': data.get('subject'),
                'email': data.get('email'),
                'message': data.get('comments')
            }, '[Website] %s contacted from Doni & Company' % data.get('name'), send_to_email=settings.EMAIL_INFO)

            return Response({'success': True, 'message': 'We have recieved your message.'}, status=status.HTTP_200_OK)
        else:
            return validated_error

    def get(self, request, *args, **kwargs):
        print 'hello--------------------------------------'
        return Response({'success': True}, status=status.HTTP_200_OK)
