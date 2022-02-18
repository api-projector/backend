AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
]

AUTH_USER_MODEL = "users.User"

ACCOUNT_USER_MODEL_USERNAME_FIELD = "login"

AUTHENTICATION_BACKENDS = [
    "apps.users.services.auth_backends.GoogleOAuth2Backend",
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = "admin:login"

TOKEN_EXPIRE_DAYS = 30
TOKEN_EXPIRE_PERIOD = 60 * 24 * TOKEN_EXPIRE_DAYS  # mins

SOCIAL_AUTH_USER_MODEL = "users.User"
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)
