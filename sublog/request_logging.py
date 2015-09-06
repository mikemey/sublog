import logging
import datetime


class RequestLoggingMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger('sublog')

    def log_message(self, method, path, response_status, time, post_msg=None):
        msg = """%s "%s" %s (%sms) """ % \
              (method, path, response_status, time)

        if post_msg:
            msg += ' post-msg: [%s]' % post_msg

        self.logger.info(msg)

    @staticmethod
    def process_request(request):
        request.logging_start_dt = datetime.datetime.utcnow()

    def process_response(self, request, response):
        method = getattr(request, 'method', 'NKN')
        path = getattr(request, 'path', 'NKN')
        status = getattr(response, 'status_code', 0)
        time = datetime.datetime.utcnow() - request.logging_start_dt

        self.log_message(method, path, status,
                         time.microseconds / 1000,
                         post_data_from(request))
        return response


def post_data_from(request):
    post_data = request.POST.get('title', None)

    if post_data:
        post_data = "title: '%s'" % post_data

    return post_data
