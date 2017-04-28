import traceback
import socket
import warnings
import md5
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
import sys
import traceback
import datetime
import json
import logging
from django.http import HttpResponse

class CrashLogMiddleware(MiddlewareMixin):
    LOGGER = logging.getLogger("django")

    def process_exception(self, request, exception):

        try:
            log = dict()
            log['request_method'] = request.method
            log['request_path'] = request.path
            log['request_path_info'] = request.path_info
            log['request_get_params'] = request.GET
            log['username'] = request.user.username
            log['business'] = request.user.profile.business.bp_name
            log['request_post_params'] = request.POST
            log['message'] = exception.message
            ex_type, ex, tb = sys.exc_info()
            log['sys_traceback'] = traceback.format_exc(tb)
            response = dict()
            response['status_code'] = 500
            response['message'] = 'Something went wrong. Please contact tramodity staff for the fix.'
            self.LOGGER.info('%s', str(log))
            return HttpResponse(content=json.dumps(response), content_type='application/json', status=500)
        except Exception, exc:
            warnings.warn(unicode(exc))