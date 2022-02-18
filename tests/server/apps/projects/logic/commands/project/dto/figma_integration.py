from dataclasses import dataclass

from rest_framework import serializers


class FigmaIntegrationDtoValidator(serializers.Serializer):
    """Create project input."""

    token = serializers.CharField(required=False)


@dataclass(frozen=True)
class FigmaIntegrationDto:
    """Figma integration data."""

    token: str
