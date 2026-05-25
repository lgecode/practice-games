from django.db import models
from django.utils.translation import gettext_lazy as _


class PokemonType(models.TextChoices):
    NORMAL = "normal", _("normal")  # 一般
    FIRE = "fire", _("fire")  # 火
    WATER = "water", _("water")  # 水
    ELECTRIC = "electric", _("electric")  # 電
    GRASS = "grass", _("grass")  # 草
    ICE = "ice", _("ice")  # 冰
    FIGHTING = "fighting", _("fighting")  # 格鬥
    POISON = "poison", _("poison")  # 毒
    GROUND = "ground", _("ground")  # 地面
    FLYING = "flying", _("flying")  # 飛行
    PSYCHIC = "psychic", _("psychic")  # 超能力
    BUG = "bug", _("bug")  # 蟲
    ROCK = "rock", _("rock")  # 岩石
    GHOST = "ghost", _("ghost")  # 幽靈
    DRAGON = "dragon", _("dragon")  # 龍
    DARK = "dark", _("dark")  # 惡
    STEEL = "steel", _("steel")  # 鋼
    FAIRY = "fairy", _("fairy")  # 妖精


class Speciality(models.TextChoices):
    GROW = "grow", _("grow")  # 栽培
    LITTER = "litter", _("litter")  # 亂撒
    BURN = "burn", _("burn")  # 點火
    FLY = "fly", _("fly")  # 飛翔
    WATER = "water", _("water")  # 滋潤
    TRADE = "trade", _("trade")  # 交易
    SEARCH = "search", _("search")  # 找東西
    CHOP = "chop", _("chop")  # 伐木
    HYPE = "hype", _("hype")  # 帶動氣氛
    YAWN = "yawn", _("yawn")  # 哈欠
    TELEPORT = "teleport", _("teleport")  # 瞬間移動
    GENERATE = "generate", _("generate")  # 發電
    RECYCLE = "recycle", _("recycle")  # 回收利用
    CRUSH = "crush", _("crush")  # 碾壓
    BULLDOZE = "bulldoze", _("bulldoze")  # 重踏
    BUILD = "build", _("build")  # 建造
    APPRAISE = "appraise", _("appraise")  # 鑑定
    UNKNOWN = "unknown", _("unknown")  # 不明
    TRANSFORM = "transform", _("transform")  # 變身
    STORAGE = "storage", _("storage")  # 收納
    GATHER_HONEY = "gather_honey", _("gather_honey")  # 採蜜
    DREAM_ISLAND = "dream_island", _("dream_island")  # 夢島
    GATHER = "gather", _("gather")  # 分類
    ILLUMINATE = "illuminate", _("illuminate")  # 發光
    EXPLODE = "explode", _("explode")  # 爆炸
    EAT = "eat", _("eat")  # 貪吃鬼
    PAINT = "paint", _("paint")  # 彩繪
    DJ = "dj", _("dj")  # DJ
    PARTY = "party", _("party")  # 開派對
    COLLECT = "collect", _("collect")  # 收藏家
    RARIFY = "rarify", _("rarify")  # 稀有物
    ENGINEER = "engineer", _("engineer")  # 工匠


class TimeOfDay(models.TextChoices):
    DAWN = "dawn", _("dawn")  # 黎明
    DAYTIME = "daytime", _("daytime")  # 白天
    DUSK = "dusk", _("dusk")  # 黃昏
    NIGHTTIME = "nighttime", _("nighttime")  # 夜晚


class Weather(models.TextChoices):
    SUNNY = "sunny", _("sunny")  # 晴天
    CLOUDY = "cloudy", _("cloudy")  # 陰天
    RAINY = "rainy", _("rainy")  # 雨天


class Environment(models.TextChoices):
    BRIGHT = "bright", _("bright")  # 明亮
    DARK = "dark", _("dark")  # 昏暗
    HUMID = "humid", _("humid")  # 潮濕
    DRY = "dry", _("dry")  # 乾燥
    WARM = "warm", _("warm")  # 溫暖
    COOL = "cool", _("cool")  # 涼爽


class Flavor(models.TextChoices):
    SPICY = "spicy", _("spicy")  # 辣辣的
    DRY = "dry", _("dry")  # 澀澀的
    SWEET = "sweet", _("sweet")  # 甜甜的
    BITTER = "bitter", _("bitter")  # 苦苦的
    SOUR = "sour", _("sour")  # 酸酸的


class NameNaturalKeyManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class PokemonType(models.Model):
    objects = NameNaturalKeyManager()
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    name_zh_hant = models.CharField(max_length=50, unique=True)
    name_en = models.CharField(max_length=50, unique=True)
    name_jp = models.CharField(max_length=50, unique=True)

    def natural_key(self):
        return (self.slug,)

    def __str__(self):
        return self.name_en


class Specialty(models.Model):
    objects = NameNaturalKeyManager()
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    name_zh_hant = models.CharField(max_length=50, unique=True)
    name_en = models.CharField(max_length=50, unique=True)
    name_jp = models.CharField(max_length=50, unique=True)

    def natural_key(self):
        return (self.slug,)

    def __str__(self):
        return self.name_en


class Habitat(models.Model):
    objects = NameNaturalKeyManager()

    name = models.CharField(max_length=100, unique=True)

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    objects = NameNaturalKeyManager()

    name = models.CharField(max_length=100, unique=True)

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name


# 寶可夢
class Pokemon(models.Model):
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True
    )
    pokopia_dex_number = models.PositiveSmallIntegerField()  # Pokopia圖鑑編號
    name = models.CharField(_("name"),
                            max_length=100
                            )
    name_chinese = models.CharField(_("name_chinese"), max_length=100, blank=True, default="")
    name_english = models.CharField(_("name_english"), max_length=100, blank=True, default="")
    name_japanese = models.CharField(_("name_japanese"), max_length=100, blank=True, default="")
    classification = models.CharField(_("classification"), max_length=50, blank=True, default="")  # 分類
    classification_chinese = models.CharField(_("classification_chinese"), max_length=100, blank=True, default="")
    classification_english = models.CharField(_("classification_english"), max_length=100, blank=True, default="")
    classification_japanese = models.CharField(_("classification_japanese"), max_length=100, blank=True, default="")
    description = models.TextField(_("description"), blank=True, default="")  # 描述
    description_chinese = models.TextField(_("description_chinese"), blank=True, default="")
    description_english = models.TextField(_("description_english"), blank=True, default="")
    description_japanese = models.TextField(_("description_japanese"), blank=True, default="")
    height = models.DecimalField(_("height"), max_digits=5, decimal_places=2, blank=True, null=True)  # 身高
    weight = models.DecimalField(_("weight"), max_digits=5, decimal_places=2, blank=True, null=True)  # 體重
    types = models.ManyToManyField(PokemonType, verbose_name=_("types"))  # 屬性
    time_of_day = models.JSONField(_("time_of_day"), blank=True, default=list)  # 能遇見的時間
    weather = models.JSONField(_("weather"), blank=True, default=list)  # 能遇見的天氣
    habitats = models.ManyToManyField(Habitat, verbose_name=_("habitats"))  # 會出現的棲地
    specialties = models.ManyToManyField(Specialty, verbose_name=_("specialties"))  # 專長
    preferred_environment = models.CharField(
        max_length=20, choices=Environment.choices, blank=True, default="", verbose_name=_("preferred_environment")
    )  # 喜歡的環境
    favorites = models.ManyToManyField(Favorite, verbose_name=_("favorites"))  # 喜歡的東西
    flavor = models.CharField(
        max_length=20, choices=Flavor.choices, blank=True, default="", verbose_name=_("flavor")
    )  # 喜歡的口味
    is_unique_npc = models.BooleanField(default=False, verbose_name=_("is_unique_npc"))  # 是否為特殊 NPC 寶可夢
    is_event = models.BooleanField(default=False, verbose_name=_("is_event"))  # 是否為活動限定寶可夢
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ItemCategory(models.TextChoices):
    FURNITURE = "furniture", _("furniture")  # 家具
    MISC = "misc", _("misc")  # 雜貨
    OUTDOOR = "outdoor", _("outdoor")  # 戶外
    UTILITIES = "utilities", _("utilities")  # 實用
    BUILDINGS = "buildings", _("buildings")  # 建築
    BLOCKS = "blocks", _("blocks")  # 方塊
    KITS = "kits", _("kits")  # 套組
    NATURE = "nature", _("nature")  # 大自然
    FOOD = "food", _("food")  # 食物    
    MATERIALS = "materials", _("materials")  # 材料
    KEY_ITEMS = "key_items", _("key_items")  # 重要的東西
    OTHER = "other", _("other")  # 其他
    UNLISTED = "unlisted", _("unlisted")  # 不在收藏圖鑑內的物品
    LOST_RELICS_L = "lost_relics_l", _("lost_relics_l")  # 大遺失物
    LOST_RELICS_S = "lost_relics_s", _("lost_relics_s")  # 小遺失物
    FOSSILS = "fossils", _("fossils")  # 化石


class ItemTag(models.TextChoices):
    FOOD = "food", _("food")  # 食物
    DECORATION = "decoration", _("decoration")  # 裝飾
    RELAXATION = "relaxation", _("relaxation")  # 休憩
    TOY = "toy", _("toy")  # 玩具
    ROAD = "road", _("road")  # 道路


class Item(models.Model):
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True
    )
    category = models.CharField(
        max_length=50, choices=ItemCategory.choices, default=ItemCategory.OTHER
    )
    name = models.CharField(_("name"),
                            max_length=150
                            )
    name_chinese = models.CharField(max_length=150, blank=True, default="")
    name_english = models.CharField(_("name_english"), max_length=150, blank=True, default="")
    name_japanese = models.CharField(_("name_japanese"), max_length=150, blank=True, default="")
    description = models.TextField(_("description"), blank=True, default="")
    description_chinese = models.TextField(_("description_chinese"), blank=True, default="")
    description_english = models.TextField(_("description_english"), blank=True, default="")
    description_japanese = models.TextField(_("description_japanese"), blank=True, default="")
    tag = models.CharField(_("tag"), max_length=30, choices=ItemTag.choices, blank=True, default="")
    favorites = models.ManyToManyField(Favorite, verbose_name=_("favorites"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name
