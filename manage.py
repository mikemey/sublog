#!/usr/bin/env python
import os
import sys
import signal

from sublog import wsgi


def signal_term_handler(rec_signal, frame):
    wsgi.shutdown_hook()
    sys.exit(0)


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sublog.settings")

    signal.signal(signal.SIGTERM, signal_term_handler)
    execute_from_command_line(sys.argv)
