
from django.conf import settings
from kernel.dependencies.django_settings import django_settings_check_keys

# -> check for required settings
django_settings_check_keys([
    'AWS_IA_SERVER_URL',
    'TEST_TRANSCRIPT_SERVER_URL',
])

