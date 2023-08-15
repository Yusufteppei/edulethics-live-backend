from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/




# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "djoser",
    "authentication.apps.AuthenticationConfig",
    "configurations",
    "corsheaders",

    #"rest_framework_api_key",
    "clearcache",
    "address",
    'fintech',    
    'django_summernote',
    "rest_framework",
#    'django_admin_caching',
    "customer_relations.apps.CustomerRelationsConfig",
    "chat",
    "notification",
    "import_export",
    "exam.apps.ExamConfig",

]

IMPORT_EXPORT_USE_TRANSACTIONS = True

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "edulethics.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "edulethics.wsgi.application"


###########################################################################################
###########################     DATABASE CONFIGURATION      ###############################

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "edulethics",
        "HOST": '163.123.183.90',
        "PORT": "19207",
        "PASSWORD": 'EdulethicsDevelopmentSafety23!',
        "USER": 'Yusuff',
    },
}

##########################################################################################
##########################################################################################


#####################################   PASSWORD VALIDATION ##############################

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

##################################      PASSWORD VALIDATION END     ##################################




####################################     INTERNATIONALIZATION    ########################

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = False


###################################     INTERNATIONALIZATION END       ####################################




####################################        STATIC/ MEDIA FILES    ###############################################

STATIC_URL = "static/"

# LINODE STORAGE SETTINGS
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

LINODE_BUCKET=os.environ.get('LINODE_BUCKET')
LINODE_BUCKET_REGION=os.environ.get('LINODE_BUCKET_REGION')
LINODE_BUCKET_ACCESS_KEY=os.environ.get('LINODE_BUCKET_ACCESS_KEY') 
LINODE_BUCKET_SECRET_KEY=os.environ.get('LINODE_BUCKET_SECRET_KEY') 


AWS_S3_ENDPOINT_URL=f'https://{LINODE_BUCKET_REGION}.linodeobjects.com'
AWS_ACCESS_KEY_ID=LINODE_BUCKET_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=LINODE_BUCKET_SECRET_KEY
AWS_S3_REGION_NAME=LINODE_BUCKET_REGION
AWS_S3_USE_SSL=True
AWS_STORAGE_BUCKET_NAME=LINODE_BUCKET

####################################        STATIC FILES END    ###########################################


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



####################################        AUTHENTICATION/ AUTHORIZATION      ##########################################
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '/username/reset/confirm/{uid}/{token}',
    #'ACTIVATION_URL': '#/activate/{uid}/{token}',
    #'SEND_ACTIVATION_EMAIL': True,

    'LOGIN_FIELD': 'username',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    #'SEND_CONFIRMATION_EMAIL': True,
    'SET_USERNAME_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,



    'SERIALIZERS': {
        'user_create': 'authentication.serializers.UserCreateSerializer',
        'user': 'authentication.serializers.UserCreateSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer'
    }
}

AUTH_USER_MODEL = 'authentication.UserAccount'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        #"rest_framework_api_key.permissions.HasAPIKey",
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100000/day',
        'user': '1000000/day'
    }
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=40),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=360),
}

################################################    AUTHENTICATION/ AUTHORIZATION END    ####################





################################################    MEDIA SETTINGS  #####################################
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

SUMMERNOTE_THEME = 'bs4'  # Show summernote with Bootstrap4

SUMMERNOTE_CONFIG = {
    'iframe': True,

    # Or, you can set it to `False` to use SummernoteInplaceWidget by default - no iframe mode
    # In this case, you have to load Bootstrap/jQuery sources and dependencies manually.
    # Use this when you're already using Bootstrap/jQuery based themes.
    #'iframe': False,

    # You can put custom Summernote settings
    'summernote': {
        # As an example, using Summernote Air-mode
        'airMode': False,

        # Change editor size
        'width': '100%',
        'height': '480',

        # Use proper language setting automatically (default)
        'lang': 'en-US',

        # Toolbar customization
        # https://summernote.org/deep-dive/#custom-toolbar-popover
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', [ 'picture', ]], # CAN ALSO ADD 'video', 'link',
            ['view', ['fullscreen', 'codeview', 'help']],
        ],

        # Or, explicitly set language/locale for editor
        #'lang': 'ko-KR',
        

        # You can also add custom settings for external plugins
        #'print': {
        #    'stylesheetUrl': '/some_static_folder/printable.css',
        #},
        #'codemirror': {
        #    'mode': 'htmlmixed',
        #    'lineNumbers': 'true',
        #    # You have to include theme file in 'css' or 'css_for_inplace' before using it.
        #    'theme': 'monokai',
        #},
    },

    # Require users to be authenticated for uploading attachments.
    'attachment_require_authentication': True,

    # Set `upload_to` function for attachments.
    #'attachment_upload_to': my_custom_upload_to_func(),

    # Set custom storage class for attachments.
    #'attachment_storage_class': 'my.custom.storage.class.name',

    # Set custom model for attachments (default: 'django_summernote.Attachment')
    #'attachment_model': 'my.custom.attachment.model', # must inherit 'django_summernote.AbstractAttachment'

    # You can completely disable the attachment feature.
    'disable_attachment': False,

    # Set to `True` to return attachment paths in absolute URIs.
    'attachment_absolute_uri': False,

    # test_func in summernote upload view. (Allow upload images only when user passes the test)
    # https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin
    
    #def example_test_func(request):
    #    return request.user.groups.filter(name='group_name').exists()
    #
   # 'test_func_upload_view': example_test_func,
}

X_FRAME_OPTIONS = 'SAMEORIGIN'
################################################    MEDIA SETTINGS END  ###################################


###############################################     ENVIRONMENT VARIABLES   ##############################

MAXIMUM_REGISTRATION_COUNT = 5

MAXIMUM_FREE_PAYMENTS = 1

#SECRET_KEY = "django-insecure-abx0bfbmaa661otm*g$oul)1%iq&+o_15%6#8m@raz%scfnh=j"

###############################################     ENVIRONMENT VARIABLES END ##############################

SECRET_KEY = os.environ.get('BACKEND_SECRET_KEY')

################################################        SECURITY    ######################################
#   HTTPS SETTINGS

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

#   HSTS SETTINGS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True


DEBUG = True

ALLOWED_HOSTS = ['172.105.15.154', 'backend.edulethics.com', 'backend.eduethics.com']

#CORS_ALLOWED_ORIGINS = [
#    'http://127.0.0.1:3000',
#    'http://10.6.112.211'
#]

CORS_ALLOW_ALL_ORIGINS = True

#CSRF_TRUSTED_ORIGINS = [
##    "http://127.0.0.1",
#    'http://10.6.112.211'
#]

################################################        SECURITY  END  ######################################

# EMAIL BACKEND

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'edulethicsdevelopment@gmail.com'
EMAIL_HOST_PASSWORD = 'adetokunboyusuf'
EMAIL_USE_TLS = True

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://0.0.0.0:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CACHE_TTL = 60 * 60 * 10

#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
#        'LOCATION': '0.0.0.0:11211',
#    }
#

FIXTURE_DIRS = (
   os.path.join(BASE_DIR, 'fixtures'),
)
