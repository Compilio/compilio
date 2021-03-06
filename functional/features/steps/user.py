from behave import *
from django.contrib.auth.models import User


def parse_optional(text):
    return text.strip()

parse_optional.pattern = r'\s?\w*\s?'
register_type(optional=parse_optional)


@given('user {username} exists')
def impl(context, username):
    User.objects.create_user(username=username,
                             email=username + '@example.com',
                             password='password')


@then('user {username} should {negation:optional}exists')
def impl(context, username, negation):
    if negation == 'not':
        assert not User.objects.filter(username=username).exists(), \
            'User %r does exist' % username
    else:
        assert User.objects.filter(username=username).exists(), \
            'User %r does not exist' % username
