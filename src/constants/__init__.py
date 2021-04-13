from enum import Enum


class ReleaseInfoStatus(Enum):
    SAME = 1
    NEW_RELEASE = 2
    DELAY = 3
    STALLED = 4
    ALTER = 5


class SourceSite(Enum):
    GSC = 1
    ALTER = 2


class BrandHost(str, Enum):
    GSC = "goodsmile.info"
    ALTER = "alter-web.jp"


class GSCCategory(str, Enum):
    SCALE = "scale"
    NENDOROID = "nendoroid_series"
    FIGMA = "figma"
    OTHER_FIGURE = "other_figures"
    GOODS = "goods_other"


class AlterCategory(str, Enum):
    FIGURE = "figure"
    ALTAIR = "altair"
    COLLABO = "collabo"
    OTHER = "other"
    ALMECHA = "almecha"


class GSCLang(str, Enum):
    ENGLISH = "en"
    JAPANESE = "ja"
    TRADITIONAL_CHINESE = "zh"
