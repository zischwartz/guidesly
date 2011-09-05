
import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG
TASTYPIE_FULL_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
from os.path import abspath, dirname, join

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(os.path.join(os.path.dirname(__file__), 'apps')) 
sys.path.insert(0, join(SITE_ROOT, "apps"))


DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'djangostack',
        'HOST': '/opt/bitnami/postgresql',
        'PORT': '5432',
        'USER': 'bitnami',
        'PASSWORD': '1d62ddfc22'
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# MEDIA_ROOT = os.path.join(SITE_ROOT, 'userstatic')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
# MEDIA_URL = '/usermedia/'
MEDIA_URL = 'http://guideslybetauserfiles.s3.amazonaws.com/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'sitestatic')
#STATIC_ROOT = '/home/zazerr/webapps/static_g/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/media/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Additional locations of static files
# We're not really using this....
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'sitestatic22'),
    
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c*48h#!%y8(@lkasi*xs%m#s+kp&cf6e-&0sot8trzh-yjvd4i'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',      
   
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',           
	'django.middleware.csrf.CsrfViewMiddleware',    
	'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'Project.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
    os.path.join(SITE_ROOT, 'templates/site/'),

    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# AWS_ACCESS_KEY_ID = 'AKIAJRCNWZLCRGKOA7FA'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_STORAGE_BUCKET_NAME= 'guideslybetauserfiles'


#*********************
# DEBUG TURNED IT OFF
# *****************
DEFAULT_FILE_STORAGE = 'apps.cuddlybuddly.storage.s3.S3Storage'



AWS_ACCESS_KEY_ID = 'AKIAJRCNWZLCRGKOA7FA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME= 'guideslybetauserfiles'
                                                 
#AUTHENTICATION_BACKENDS='django.contrib.auth.backends.ModelBackend'
#AUTHENTICATION_BACKENDS= 'object_permissions.backend.ObjectPermBackend',

# got Error importing authentication backends. Is AUTHENTICATION_BACKENDS a correctly defined list or tuple?
# commented this out, loaded page, commented back in, everything is fine?

AWS_HEADERS = [
    ('^private/', {
        'x-amz-acl': 'private',
        'Expires': 'Thu, 15 Apr 2000 20:00:00 GMT',
        'Cache-Control': 'private, max-age=0'
    }),
    ('.*', {
        'x-amz-acl': 'public-read',
        'Expires': 'Sat, 30 Oct 2010 20:00:00 GMT',
        'Cache-Control': 'public, max-age=31556926'
    })
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',

    'object_permissions',
    'tagging',
	'invitation',
	'registration',
	'thef',
    'accounts',
    'tastypie',
    # 'apps.cuddlybuddly.storage.s3',
    # 'debug_toolbar',
    'south',


	'fileupload',
    'guides',

)                  
            
AUTH_PROFILE_MODULE = 'accounts.userprofile'

INVITE_MODE = True 

ACCOUNT_ACTIVATION_DAYS = 5

ACCOUNT_INVITATION_DAYS = 7

INVITATIONS_PER_USER = 0   

LOGIN_REDIRECT_URL = '/home/'

LOG_FILE = os.path.join(SITE_ROOT, 'log.log')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     }
# }


# DEBUG_TOOLBAR_PANELS = (
#     'debug_toolbar.panels.version.VersionDebugPanel',
#     'debug_toolbar.panels.timer.TimerDebugPanel',
#     'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#     'debug_toolbar.panels.headers.HeaderDebugPanel',
#     'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#     'debug_toolbar.panels.template.TemplateDebugPanel',
#     'debug_toolbar.panels.sql.SQLDebugPanel',
#     'debug_toolbar.panels.signals.SignalDebugPanel',
#     'debug_toolbar.panels.logger.LoggingPanel',
# )  

# DEBUG_TOOLBAR_CONFIG = {
#     'INTERCEPT_REDIRECTS': False,
#     'HIDE_DJANGO_SQL': False,
# }

EMAIL_HOST = 'smtp.gmail.com'     

EMAIL_HOST_USER = 'invite@guidesly.com'

EMAIL_HOST_PASSWORD = 'dogsarecoolyo'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

try:
   from settings_local import *
except ImportError, e:
   pass
