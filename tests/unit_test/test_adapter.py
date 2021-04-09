from datetime import date, datetime

import pytest

from src.Adapters import ReleaseToProductReleaseInfoModelAdapter
from src.custom_classes import OrderPeriod, Release
from src.Models import Product, ProductReleaseInfo


@pytest.mark.usefixtures("session")
def test_Release_to_ProductReleaseInfoModel(session):
    p = Product(name="foo")
    release = Release(
        release_date=date(2020, 1, 1),
        price=12000,
        order_period=OrderPeriod(
            datetime(2019, 12, 1, 12, 0),
            datetime(2019, 12, 31, 23, 59)
        )
    )
    release_adapter = ReleaseToProductReleaseInfoModelAdapter(release)
    assert isinstance(release_adapter, ProductReleaseInfo)

    # prevent IntegrityError from sqlalchemy
    # because the `product_id` should be NOT NULL
    # info: sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: product_release_info.product_id
    p.release_infos.append(release_adapter)
    p.save()
    session.commit()

    fetched_info = ProductReleaseInfo.first()
    assert fetched_info
