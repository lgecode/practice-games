from bisect import bisect_right
from warnings import WarningMessage
from django.db import models


class GameLanguage(models.TextChoices):
    ENGLISH = "en", "English"
    JAPANESE = "ja", "Japanese"
    TRADITIONAL_CHINESE = "zh-Hant", "Traditional Chinese"


class TimeOfDay(models.TextChoices):
    DAWN = "黎明", "黎明"  # Dawn
    DAYTIME = "白天", "白天"  # Daytime
    DUSK = "黃昏", "黃昏"  # Dusk
    NIGHTTIME = "夜晚", "夜晚"  # Nighttime
    

class Weather(models.TextChoices):
    SUNNY = "晴天", "晴天"  # Sunny
    CLOUDY = "陰天", "陰天"  # Cloudy
    RAINY = "雨天", "雨天"  # Rainy

class Environment(models.TextChoices):
    BRIGHT = "明亮", "明亮"  # Bright
    DARK = "昏暗", "昏暗"  # Dark
    HUMID = "潮濕", "潮濕"  # Humid
    DRY = "乾燥", "乾燥"  # Dry
    WARM = "溫暖", "溫暖"  # Warm
    COOL = "涼爽", "涼爽"  # Cool


class Flavor(models.TextChoices):
    SPICY = "辣辣的", "辣辣的"  # Spicy
    DRY = "澀澀的", "澀澀的"  # Dry
    SWEET = "甜甜的", "甜甜的"  # Sweet
    BITTER = "苦苦的", "苦苦的"  # Bitter
    SOUR = "酸酸的", "酸酸的"  # Sour


class NameNaturalKeyManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class PokemonType(models.Model):
    objects = NameNaturalKeyManager()

    name = models.CharField(max_length=50, unique=True)

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name

class Habitat(models.Model):
    objects = NameNaturalKeyManager()

    name = models.CharField(max_length=100, unique=True)

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name

class Specialty(models.Model):
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
    # slug = models.SlugField(
    #     max_length=100, unique=True, blank=True, null=True
    # )  # 穩定識別用代稱，適合網址、匯入資料或程式查找
    pokopia_dex_number = models.PositiveSmallIntegerField()  # Pokopia圖鑑編號
    name = models.CharField(
        max_length=100
    )
    classification = models.CharField(max_length=50, blank=True, default="")  # 分類
    description = models.TextField(blank=True, default="")  # 描述
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # 身高
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # 體重
    types = models.ManyToManyField(PokemonType)  # 屬性
    time_of_day = models.JSONField(blank=True, default=list) # 能遇見的時間
    weather = models.JSONField(blank=True, default=list) # 能遇見的天氣
    habitats = models.ManyToManyField(Habitat)  # 會出現的棲地
    specialties = models.ManyToManyField(Specialty)  # 專長
    preferred_environment = models.CharField(
        max_length=20, choices=Environment.choices, blank=True, default=""
    )  # 喜歡的環境
    favorites = models.ManyToManyField(Favorite)    # 喜歡的東西
    flavor = models.CharField(
        max_length=20, choices=Flavor.choices, blank=True, default=""
    )  # 喜歡的口味
    is_unique_npc = models.BooleanField(default=False)  # 是否為特殊 NPC 寶可夢
    is_event = models.BooleanField(default=False)  # 是否為活動限定寶可夢
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ItemCategory(models.TextChoices):
    MATERIAL = "材料", "材料"
    FOOD = "食物", "食物"
    FURNITURE = "傢俱", "傢俱"
    GOODS = "雜貨", "雜貨"
    OUTDOOR = "戶外", "戶外"
    PRACTICAL = "實用", "實用"
    NATURE = "自然", "自然"  # 大自然?
    BUILDING = "建築", "建築"
    BLOCK = "方塊", "方塊"
    SET = "套組", "套組"
    KEY_ITEM = "重要的物品", "重要的物品"
    OTHER = "其他", "其他"
    UNLISTED = "不在收藏圖鑑內的物品", "不在收藏圖鑑內的物品"


class ItemTag(models.TextChoices):
    FOOD = "食物", "食物"
    DECORATION = "裝飾", "裝飾"
    REST = "休憩", "休憩"
    TOY = "玩具", "玩具"
    ROAD = "道路", "道路"


class Item(models.Model):
    # slug = models.SlugField(
    #     max_length=150, unique=True, blank=True, null=True
    # )  # 穩定識別用代稱，適合網址、匯入資料或程式查找
    category = models.CharField(
        max_length=20, choices=ItemCategory.choices, default=ItemCategory.OTHER
    )
    name = models.CharField(
        max_length=150
    )
    description = models.TextField(blank=True, default="")
    tag = models.CharField(max_length=30, choices=ItemTag.choices, blank=True, default="")
    favorites = models.ManyToManyField(Favorite)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name