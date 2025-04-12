class MissingAnnotationError(AttributeError):
    """
    Raised when an expected annotated field is missing from a model instance.

    This is useful for catching developer errors when a serializer relies on
    fields that must be annotated via `.annotate(...)` in the queryset.

    The exception mimics the standard AttributeError format to provide a
    familiar and descriptive error message.

    Example:
        raise MissingAnnotationError(instance, "some_field")
    """

    def __init__(self, instance: object, field_name: str) -> None:
        cls_name = type(instance).__name__
        message = (
            f"'{cls_name}' missing required annotated field: '{field_name}'"
        )
        super().__init__(message)
