from typing import Annotated

from pydantic.functional_serializers import PlainSerializer


def serialize_list(value: list[str] | None) -> str | None:
    """
    List of strings serialization.

    Serialize a list of objects into a
    string of strings separated by commas.
    """
    if value is not None:
        return ",".join(value)
    return value


type CommaList[T] = Annotated[
    list[T],
    PlainSerializer(serialize_list, str | None),
]
