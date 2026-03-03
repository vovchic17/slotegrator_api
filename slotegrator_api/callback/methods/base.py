import inspect

from fastapi import Form
from pydantic import BaseModel


class SlotegratorCallback(BaseModel):
    """Slotegrator callback base model."""

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__()
        fields = cls.__annotations__
        parameters = [
            inspect.Parameter(
                field_name,
                inspect.Parameter.KEYWORD_ONLY,
                annotation=field_type,
                default=Form(),
            )
            for field_name, field_type in fields.items()
        ]

        def as_form[T](cls: type[T], **kwargs: object) -> T:
            return cls(**kwargs)

        as_form.__signature__ = inspect.Signature(parameters=parameters)  # type: ignore[attr-defined]
        cls.as_form = as_form  # type: ignore[attr-defined]

    action: str
