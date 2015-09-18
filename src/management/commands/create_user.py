from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a user'

    def handle(self, *args, **options):
        print '\nCreating a new user, I\'ll ask you following fields:'
        print '\tUser name   -    (required) Human readable identifier of user (must be unique).'
        print '\tPassword    -    (required) Password'
        print '\tFirst name  -    (optional) First name, visible on web page.'
        print '\tEmail       -    (optional) Email address, only used for notification emails.'
        print '\n'

        user_name = None
        name_exists = True
        while name_exists:
            user_name = self.read_user_input('User name')
            name_exists = self.does_name_exist(user_name)
            if name_exists:
                print 'Username already exists: %s' % user_name

        password = self.read_user_input('Password')
        first_name = self.read_user_input('First name', True)
        email = self.read_user_input('Email', True)

        print '\nPlease confirm:'
        print 'User name : %s' % user_name
        print 'Password  : %s' % password
        print 'First name: %s' % first_name
        print 'Email     : %s' % email

        if self.read_user_input('correct [y/n]') == 'y':
            print 'creating user...'
            self.create_user(user_name, password, first_name, email)
        else:
            print 'create user aborted!'

        print 'finished'

    @staticmethod
    def does_name_exist(user_name):
        try:
            User.objects.get_by_natural_key(user_name)
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def create_user(user, password, first_name, email):
        user = User.objects.create_user(user, email, password, first_name=first_name)
        user.save()

    @staticmethod
    def read_user_input(label, none_allowed=False):
        user_input = None
        valid_input = False
        while not valid_input:
            user_input = raw_input(' %s: ' % label)
            if user_input or none_allowed:
                valid_input = True
            else:
                print 'Field is mandatory: %s' % label

        return user_input
