from dataclasses import dataclass

from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.core.logic import messages
from apps.core.services.image.cropper import CroppingParameters, crop_image
from apps.media.models import Image
from apps.users.models import User


@dataclass(frozen=True)
class CommandResult:
    """Upload image command result."""

    image: Image


@dataclass(frozen=True)
class UploadImageDto:
    """Upload image dto."""

    file: InMemoryUploadedFile  # noqa: WPS110
    left: int
    top: int
    width: int
    height: int
    scale: float


class Command(messages.BaseCommand[CommandResult]):
    """Upload image command."""

    user: User
    image_data: UploadImageDto


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Uploading image."""

    def handle(self, command: Command) -> CommandResult:
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
