from datetime import date, datetime

from babel.dates import format_date
from discord import Colour, Embed

embed_templates = {
    "en": {
        "maker": "Manufacturer",
        "series": "Series",
        "price": "Price",
        "release_date": "Release Date",
        "sculptors": "Sculptors",
        "paintworks": "Paintworks",
        "date_format": "MMM, yyyy"
    },
    "ja": {
        "maker": "メーカー",
        "series": "作品名",
        "price": "価格",
        "release_date": "発売時期",
        "sculptors": "原型制作",
        "paintworks": "彩色",
        "date_format": "yyyy年 MMM",
    },
    "zh-TW": {
        "maker": "製造商",
        "series": "作品名稱",
        "price": "價格",
        "release_date": "發售日期",
        "sculptors": "原型製作",
        "paintworks": "色彩",
        "date_format": "yyyy年 MMM",
    },
}

locale_mapping = {
    "en": "en",
    "ja": "ja",
    "zh-TW": "zh"
}


class NewReleaseEmbed(Embed):
    _is_nsfw: bool

    def __init__(self, **kwargs):
        kwargs.setdefault("colour", Colour.red())
        super().__init__(**kwargs)
        self._is_nsfw = kwargs.get("is_nsfw", False)

    @property
    def is_nsfw(self):
        return self._is_nsfw

    def localized_with(self, lang: str):
        """lang: en, ja, zh-TW"""
        embed = self.copy()
        for f in embed._fields:
            key = f["name"]
            f["name"] = embed_templates[lang].get(key, key)
            if key == "release_date":
                locale = locale_mapping.get(lang, "en")
                date_format = embed_templates[lang]["date_format"]
                release_date = datetime.strptime(f["value"], "%Y-%m-%d").date()
                f["value"] = str(format_date(release_date, date_format, locale=locale))

        return embed


class DiscordEmbedFactory:
    @staticmethod
    def create_new_release(
        name: str,
        url: str,
        series: str,
        maker: str,
        price: int,
        image: str,
        release_date: date,
        thumbnail: str,
        is_adult: bool,
    ):
        embed = NewReleaseEmbed(title=name, type="rich", url=url, is_nsfw=is_adult)
        embed.set_image(url=image)
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(
            name="maker", value=maker, inline=False
        ).add_field(
            name="series", value=series, inline=False
        ).add_field(
            name="price", value=f"JPY {price:,}", inline=True
        ).add_field(
            name="release_date", value=release_date, inline=True
        )
        return embed

    @staticmethod
    def create_new_hook_notification(msg: str):
        title = f":hook: {msg} :hook:"
        embed = Embed(title=title, colour=Colour(0x00B5FF))

        return embed
