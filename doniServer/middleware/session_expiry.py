from django.utils.deprecation import MiddlewareMixin


class SessionExpiry(MiddlewareMixin):
    SESSION_EXPIRY = 15 * 60

    def process_response(self, request, response):
        if hasattr(request, 'user') and request.user.is_authenticated():
            request.session.set_expiry(self.SESSION_EXPIRY)
        return response

