import re
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date
from typing import Optional, Union, overload

from src.custom_classes import HistoricalReleases, OrderPeriod, Release

__all__ = [
    "ProductBase",
    "ProductDataProcessMixin",
    "ProductUtils"
]


@dataclass
class ProductBase:
    __slots__ = (
        "url",
        "name",
        "series",
        "manufacturer",
        "category",
        "price",
        "release_date",
        "release_infos",
        "order_period",
        "size",
        "scale",
        "sculptors",
        "paintworks",
        "resale",
        "adult",
        "copyright",
        "releaser",
        "distributer",
        "jan",
        "maker_id",
        "images"
    )

    url: str
    name: str
    series: Union[str, None]
    manufacturer: str
    category: str
    price: int
    release_date: date
    release_infos: HistoricalReleases[Release]
    order_period: Optional[OrderPeriod]
    size: int
    scale: Union[int, None]
    sculptors: list[str]
    paintworks: list[str]
    resale: bool
    adult: bool
    copyright: str
    releaser: Optional[str]
    distributer: Optional[str]
    jan: Optional[str]
    maker_id: Optional[str]
    images: list[str]

    def as_dict(self) -> dict:
        return asdict(self)

    def __str__(self):
        return f"[{self.manufacturer}] {self.name} {self.category}"


class ProductDataProcessMixin:
    __slots__ = ()
    attrs_to_be_normalized: list[str] = [
        "name",
        "series",
        "manufacturer",
        "releaser",
        "distributer",
        "paintworks",
        "sculptors"
    ]

    def normalize_attrs(self: ProductBase) -> None:
        """
        normalize string attributes or string in list attributes
        + full-width (alphabet, notation) to half-width.
        + remove duplicate spaces.
        + remove some weird notations.
        """
        for attr in self.attrs_to_be_normalized:
            attr_value = getattr(self, attr)
            setattr(self, attr, ProductUtils.normalize_product_attr(attr_value))


class Product(ProductBase, ProductDataProcessMixin):
    __slots__ = ()
    ...


class ProductUtils:

    @overload
    def normalize_product_attr(attr_value: str) -> str: ...
    @overload
    def normalize_product_attr(attr_value: list[str]) -> list[str]: ...

    @staticmethod
    def normalize_product_attr(attr_value: Union[str, list[str]]):
        if not attr_value:
            return attr_value

        def normalize(value: str):
            # full-width to half-width
            value = unicodedata.normalize("NFKC", value)
            # remove weird spaces
            value = re.sub(r"\s{1,}", " ", value, 0, re.MULTILINE)
            # replace weird quotation
            value = re.sub(r"’", "'", value, 0)

            return value

        if type(attr_value) is str:
            return normalize(attr_value)

        if type(attr_value) is list:
            if all(type(v) is str for v in attr_value):
                return list(map(normalize, attr_value))

        raise TypeError("The attribute value should be `str` or `list[str]`.")
