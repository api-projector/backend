from dataclasses import asdict

import injector
from django.contrib.auth.hashers import make_password

from apps.media.logic.interfaces import IImageDownloadService
from apps.users.logic.interfaces import ISignupService
from apps.users.logic.interfaces.signup import SignupData, SocialSignupData
from apps.users.models import User


class SignupService(ISignupService):
    """Service for signup new user."""

    @injector.inject
    def __init__(
        self,
        image_service: IImageDownloadService,
    ):
        """Initialize."""
        self._image_service = image_service

    def signup(self, signup_data: SignupData) -> User:
        """Signup user by provided data."""
        user = self._create_user(
            first_name=signup_data.first_name,
            password=signup_data.password,
            email=signup_data.email,
            last_name=signup_data.last_name,
            is_staff=False,
        )

        user.set_password(signup_data.password)
        user.save()

        return user

    def signup_from_social(self, signup_data: SocialSignupData) -> User:
        """Signup user by provided data."""
        social_data = asdict(signup_data)
        avatar_url = social_data.pop("avatar", None)
        if avatar_url:
            avatar = self._image_service.download_image(avatar_url)
            if avatar:
                social_data["avatar"] = avatar

        return self._create_user(
            is_staff=False,
            **social_data,
            password=make_password(None),
        )

    def _create_user(self, **kwargs) -> User:
        """Validate and create user."""
        user = User(**kwargs)
        user.full_clean()
        user.save()

        return user
