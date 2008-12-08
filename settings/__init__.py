import os

# --------------------------------------------------------------------
# Watercooler-specific settings
# --------------------------------------------------------------------

# Find the absolute path to this project's source code (which will be
# used in the settings below).
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

# How many seconds of inactivity before a user is considered inactive?
ACTIVE_USER_TIMEOUT = 20


# --------------------------------------------------------------------
# Django settings for Watercooler
# --------------------------------------------------------------------
ADMINS = (
    ('Will McCutchen', 'mccutchen@gmail.com'),
)
MANAGERS = ADMINS

ROOT_URLCONF = 'watercooler.urls'

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
    # Adds the MEDIA_URL setting to the context
    'django.core.context_processors.media',
    # Adds the current user to the context
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


# --------------------------------------------------------------------
# Deployment-specific settings
#
# First, try importing settings for the current host.  Then try
# importing "local" settings (which wouldn't be kept under version
# control).  Ignore any errors.
# --------------------------------------------------------------------
try:
    import socket, re
    hostname = re.sub(r'[-\.]', '_', socket.gethostname())
    exec "from %s import *" % hostname
except ImportError:
    pass

# Import local settings (which aren't kept in version control)
try:
    from local import *
except ImportError:
    pass
