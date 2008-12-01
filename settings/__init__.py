import os
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

# How many seconds of inactivity before a user is considered inactive?
ACTIVE_USER_TIMEOUT = 20

ADMINS = (
    ('Will McCutchen', 'mccutchen@gmail.com'),
)
MANAGERS = ADMINS

ROOT_URLCONF = 'watercooler.urls'

AUTH_PROFILE_MODULE = 'watercooler.UserProfile'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'watercooler',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.media',
    'django.core.context_processors.auth',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

# Where to redirect the user on successful login if a "next" page
# isn't given.
LOGIN_REDIRECT_URL = '/'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True


# Import specific settings based on hostname
try:
    import socket, re
    hostname = re.sub(r'[-\.]', '_', socket.gethostname())
    exec "from %s import *" % hostname
except ImportError, e:
    raise e

# Import local settings (which aren't kept in version control)
try:
    from local import *
except ImportError:
    pass
