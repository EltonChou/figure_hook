from babel.dates import format_date

from ..extension_class import ReleaseFeed


class PlurkContentFactory:
    @staticmethod
    def create_new_release(release_feed: ReleaseFeed):
        release_date_text = "未定"
        if release_feed.release_date:
            release_date_text = format_date(
                release_feed.release_date, "YYYY年MMM", locale='zh'
            )

        content = "" \
            "[**新品速報**]\n" \
            f"商品名: [{release_feed.name}]({release_feed.url})\n" \
            f"作品名稱: {release_feed.series}\n" \
            f"製造商: {release_feed.maker}\n" \
            f"尺寸: {release_feed.size}mm\n" \
            f"發售日期: {release_date_text}\n" \
            f"價格: {release_feed.price} 日圓\n" \
            f"{release_feed.media_image}\n" \
            "----------\n" \
            "📨 [Discord 速報訂閱](https://bit.ly/3wj8Gpj)"

        return {
            "content": content,
            "qualifier": "shares",
            "porn": int(release_feed.is_adult),
            "lang": "tr_ch"
        }
