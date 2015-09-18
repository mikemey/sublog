from email.mime.text import MIMEText
import logging
import os
from smtplib import SMTP

logger = logging.getLogger('sublog.mail')


def pull_in_variables():
    import subprocess

    command = ['bash', '-c', 'source deploy/sublog_variables.sh && env']
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in proc.stdout:
        (key, _, value) = line.partition("=")
        os.environ[key] = value.strip()
    proc.communicate()


class MailSend:
    def __init__(self):
        self.params = None

    def check(self):
        if not self.params:
            pull_in_variables()
            if 'MAIL_SMTP_SERVER' not in os.environ:
                msg = "email variables not set!"
                logger.error(msg)
                raise EnvironmentError(msg)

            self.params = {
                'smtp_server': os.environ['MAIL_SMTP_SERVER'],
                'sender': os.environ['MAIL_SENDER'],

                'username': os.environ['MAIL_USERNAME'],
                'password': os.environ['MAIL_PASSWORD'],

            }

    def send(self, destination, email_subject, email_content, text_subtype='html'):
        self.check()
        try:
            msg = MIMEText(email_content, text_subtype)
            msg['Subject'] = email_subject
            msg['From'] = self.params['sender']

            conn = SMTP(self.params['smtp_server'])
            # conn.set_debuglevel(False)
            conn.login(self.params['username'], self.params['password'])
            try:
                logger.info('sending mail to: %s' % destination)
                conn.sendmail(self.params['sender'], destination, msg.as_string())
            finally:
                conn.close()
                return 0
        except Exception, exc:
            logger.info('sending failed: %s' % str(exc))
            return 1
