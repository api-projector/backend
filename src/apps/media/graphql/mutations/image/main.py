from apps.media.graphql.mutations.image import upload


class MediaMutations:
    """All media mutations."""

    upload_image = upload.UploadImageMutation.Field()
