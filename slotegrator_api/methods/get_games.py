from http import HTTPMethod
from typing import Literal, Self

from pydantic import Field, model_validator

from slotegrator_api.types import CommaList, Game, Items

from .base import SlotegratorMethod


class GetGames(SlotegratorMethod[Items[Game]]):
    """Get games method."""

    __return_type__ = Items[Game]
    __method_path__ = "/games"
    __http_method__ = HTTPMethod.GET

    expand: (
        CommaList[Literal["tags", "parameters", "images", "related_games"]]
        | None
    ) = None

    page: int | None = None

    filter_provider: str | None = Field(
        default=None,
        alias="filter[provider]",
    )

    filter_is_mobile: bool | None = Field(
        default=None,
        alias="filter[is_mobile]",
    )

    filter_has_freespins: bool | None = Field(
        default=None,
        alias="filter[has_freespins]",
    )

    @model_validator(mode="after")
    def validate_single_filter(self) -> Self:
        filters = [
            self.filter_provider,
            self.filter_is_mobile,
            self.filter_has_freespins,
        ]

        if sum(x is not None for x in filters) > 1:
            msg = "Only one filter_* field can be used at a time"
            raise ValueError(msg)

        return self

    def model_dump(self, **kwargs: object) -> dict[str, object]:
        data = super().model_dump(by_alias=True, **kwargs)  # type: ignore[arg-type]

        for key in (
            "filter[is_mobile]",
            "filter[has_freespins]",
        ):
            if key in data:
                data[key] = int(data[key])

        return data
