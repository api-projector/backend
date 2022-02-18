from dataclasses import dataclass

from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.core.logic import commands
from apps.core.services.image.cropper import CroppingParameters, crop_image
from apps.media.models import Image
from apps.users.models import User


@dataclass(frozen=True)
class UploadImageDto:
    """Upload image dto."""

    file: InMemoryUploadedFile  # noqa: WPS110
    left: int
    top: int
    width: int
    height: int
    scale: float


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Upload image command."""

    user: User
    image_data: UploadImageDto


@dataclass(frozen=True)
class CommandResult:
    """Upload image command result."""

    image: Image


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Uploading image."""

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        image_data = command.image_data

        cropped_image = crop_image(
            file_object=image_data.file,
            parameters=CroppingParameters(
                left=image_data.left,
                top=image_data.top,
                width=image_data.width,
                height=image_data.height,
                scale=image_data.scale,
            ),
        )

        return CommandResult(
            Image.objects.create(
                storage_image=cropped_image,
                created_by=command.user,
            ),
        )
