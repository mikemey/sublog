import logging
import datetime

from user_agents import parse

UNKNOWN_STRING = 'NKN'


class RequestLoggingMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger('sublog')

    def log_message(self, method, path, response_status, time, user_ip, user_agent, post_msg=None):
        msg = """%s %s %s (%sms) [%s, '%s', '%s', '%s']""" % \
              (method, path, response_status, time, user_ip,
               user_agent[0], user_agent[1], user_agent[2])

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
                         request.META['HTTP_X_FORWARDED_FOR'],
                         simple_user_agent(request),
                         post_data_from(request))
        return response


def post_data_from(request):
    post_data = request.POST.get('title', None)

    if post_data:
        post_data = "title: '%s'" % post_data

    return post_data


def simple_user_agent(request):
    full_user_agent = request.META.get('HTTP_USER_AGENT', UNKNOWN_STRING)
    if full_user_agent is not UNKNOWN_STRING:
        user_agent = parse(full_user_agent)
        os = user_agent.os.family
        device = user_agent.device.family
        browser = user_agent.browser.family
        return os, device, browser

    return UNKNOWN_STRING, UNKNOWN_STRING, UNKNOWN_STRING
