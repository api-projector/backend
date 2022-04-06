import hashlib


class Empty:
    """Represents not filled value."""

    def __deepcopy__(self, memodict):
        """No copy, but himself."""
        return self


empty = Empty()


def get_instance_hash(instance) -> str:
    """Generate md5 hash for instance based on pk."""
    return hashlib.md5(  # noqa: S303 S324
        str(instance.pk).encode(),
    ).hexdigest()


def get_string_hash(text: str) -> str:
    """Generate md5 hash for string."""
    return hashlib.md5(text.encode()).hexdigest()  # noqa: S303 S324
