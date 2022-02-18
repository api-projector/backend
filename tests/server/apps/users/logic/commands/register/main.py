from dataclasses import asdict, dataclass

import injector
from django.utils import timezone
from rest_framework import serializers

from apps.core.logic import commands
from apps.users.logic.commands.register.errors import (
    RegistrationInputError,
    UserAlreadyExistsError,
)
from apps.users.logic.interfaces import ISignupService, ITokenService
from apps.users.logic.interfaces.signup import SignupData
from apps.users.models import Token, User


class _InputValidator(serializers.Serializer):
    """Registration serializer."""

    first_name = serializers.CharField(
        max_length=50,  # noqa: WPS432
        required=True,
    )
    last_name = serializers.CharField(
        max_length=50,  # noqa: WPS432
        required=True,
    )
    email = serializers.EmailField(
        max_length=50,  # noqa: WPS432
        required=True,
    )
    password = serializers.CharField(required=True)


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Register command."""

    first_name: str
    last_name: str
    email: str
    password: str


@dataclass(frozen=True)
class CommandResult:
    """Register output dto."""

    token: Token


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Register new user."""

    @injector.inject
    def __init__(
        self,
        token_service: ITokenService,
        signup_service: ISignupService,
    ):
        """Initializing."""
        self._token_service = token_service
        self._signup_service = signup_service

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        self._validate_data(command)

        user = self._signup_service.signup(
            SignupData(
                first_name=command.first_name,
                password=command.password,
                email=command.email,
                last_name=command.last_name,
            ),
        )

        self._update_user(user)

        return CommandResult(
            token=self._token_service.create_user_token(user),
        )

    def _validate_data(self, command) -> None:
        """Validate input data."""
        serializer = _InputValidator(data=asdict(command))
        if not serializer.is_valid():
            raise RegistrationInputError()

        validated_data = serializer.validated_data

        if User.objects.filter(email=validated_data["email"]).exists():
            raise UserAlreadyExistsError()

    def _update_user(self, user: User):
        user.last_login = timezone.now()
        user.save(update_fields=("last_login",))
