from pydantic import Field

from slotegrator_api.types import SlotegratorObject


class Href(SlotegratorObject):
    """Href model."""

    href: str


class PaginationLinks(SlotegratorObject):
    """Pagination links model."""

    self: Href
    next: Href | None = None
    last: Href | None = None


class PaginationMeta(SlotegratorObject):
    """Pagination meta model."""

    total_count: int = Field(alias="totalCount")
    page_count: int = Field(alias="pageCount")
    current_page: int = Field(alias="currentPage")
    per_page: int = Field(alias="perPage")


class Items[T](SlotegratorObject):
    """Items model."""

    items: list[T]
    links: PaginationLinks = Field(alias="_links")
    meta: PaginationMeta = Field(alias="_meta")
