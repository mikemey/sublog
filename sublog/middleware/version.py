from sublog import settings

version = settings.SU_VERSION

version_data = dict([('version', version)])


def add_version(request):
    return version_data
