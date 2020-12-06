# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import re
import unicodedata
from datetime import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from src.database import session
from src.Models import (Category, Company, Paintwork, Product,
                        ProductOfficialImage, ProductReleaseInfo, Sculptor,
                        Series)


def normalize_text(v):
    v = unicodedata.normalize("NFKC", v)
    # remove weird spacec
    v = re.sub(r"\s{1,}", " ", v, 0, re.MULTILINE)
    v = re.sub(r"’", "'", v, 0)
    return v


class ProductDataProcessingPipeline:
    def process_item(self, item, spider):
        # full-width to half-width. Yeah, that's you, ＫＡＤＯＫＡＷＡ
        for key in ["manufacturer", "releaser", "distributer", "paintworks", "sculptors", "series"]:
            if isinstance(item[key], list):
                item[key] = list(map(normalize_text, item[key]))
            if isinstance(item[key], str):
                item[key] = normalize_text(item[key])

        # fill price according to release_dates
        dates_len = len(item["release_dates"])
        prices_len = len(item["prices"])
        if not prices_len:
            item["prices"] = [None] * dates_len
        if dates_len > prices_len:
            item["prices"].extend(item["prices"][-1::] * (dates_len - prices_len))
        if not dates_len:
            item["release_dates"] = [None] * prices_len
        return item


class SaveProductInDatabasePipeline:
    def __init__(self) -> None:
        self.session = session

    def process_item(self, item, spider):
        product = self.session.query(Product).filter_by(
            name=item["name"],
            id_by_official=item["maker_id"]
        ).first()

        if product:
            return item

        # unique object
        series = Series.as_unique(self.session, name=item["series"])
        manufacturer = Company.as_unique(self.session, name=item["manufacturer"])
        category = Category.as_unique(self.session, name=item["category"])
        releaser = Company.as_unique(self.session, name=item["releaser"])
        distributer = Company.as_unique(self.session, name=item["distributer"])

        product = Product(
            url=item["url"],
            name=item["name"],
            size=item["size"],
            scale=item["scale"],
            resale=item["resale"],
            adult=item["adult"],
            copyright=item["copyright"],
            series=series,
            manufacturer=manufacturer,
            releaser=releaser,
            distributer=distributer,
            category=category,
            id_by_official=item["maker_id"]
        )

        for price, date in zip(item["prices"], item["release_dates"]):
            info = ProductReleaseInfo(
                price=price,
                initial_release_date=date,
            )
            product.release_infos.append(info)

        for paintwork in item["paintworks"]:
            p = Paintwork.as_unique(self.session, name=paintwork)
            product.paintworks.append(p)

        for sculptor in item["sculptors"]:
            s = Sculptor.as_unique(self.session, name=sculptor)
            product.sculptors.append(s)

        for url in item["images"]:
            image = ProductOfficialImage(url=url)
            product.official_images.append(image)

        if len(product.release_infos):
            date = datetime.strptime(item["images"][0].split("/")[4], "%Y%m%d").date()
            product.release_infos[0].update(
                announced_at=date
            )
            if item["order_period"]:
                product.release_infos[-1].update(
                    order_period_start=item["order_period"].start,
                    order_period_end=item["order_period"].end
                )

        product.save()
        self.session.close()
        return item
