import logging

from sublog import settings

version = settings.SU_VERSION

logging.getLogger('sublog.ver').info('setting version to [%s]' % version)
version_data = dict([('version', version)])


def add_version(request):
    return version_data
