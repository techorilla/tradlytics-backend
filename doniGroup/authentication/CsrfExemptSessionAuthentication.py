from rest_framework.authentication import SessionAuthentication


# Not Performing Session Authentication
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return