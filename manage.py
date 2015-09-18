#!/usr/bin/env python
import logging
import os
import sys
import signal


def signal_term_handler(rec_signal, frame):
    logging.getLogger('sublog').info('server stopped.')
    sys.exit(0)


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sublog.settings")

    signal.signal(signal.SIGHUP, signal_term_handler)
    execute_from_command_line(sys.argv)
