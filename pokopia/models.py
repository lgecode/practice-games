from django.db import models


class GameLanguage(models.TextChoices):
    ENGLISH = "en", "English"
    JAPANESE = "ja", "Japanese"
    TRADITIONAL_CHINESE = "zh-Hant", "Traditional Chinese"
    SIMPLIFIED_CHINESE = "zh-Hans", "Simplified Chinese"
    KOREAN = "ko", "Korean"
    SPANISH = "es", "Spanish"
    FRENCH = "fr", "French"
    GERMAN = "de", "German"
    ITALIAN = "it", "Italian"



class TimeOfDay(models.TextChoices):
    DAWN = "dawn", "Dawn"
    DAYTIME = "daytime", "Daytime"
    DUSK = "dusk", "Dusk"
    NIGHTTIME = "nighttime", "Nighttime"
    

class Weather(models.TextChoices):
    SUNNY = "sunny", "Sunny"
    CLOUDY = "cloudy", "Cloudy"
    RAINY = "rainy", "Rainy"

class PokemonType(models.Model):
    name = models.CharField(max_length=50)



# 寶可夢
class Pokemon(models.Model):
    slug = models.SlugField(
        max_length=100, unique=True
    )  # 穩定識別用代稱，適合網址、匯入資料或程式查找
    pokopia_dex_number = models.PositiveSmallIntegerField()  # Pokopia圖鑑編號
    name = models.CharField(
        max_length=100
    )
    classification = models.CharField(max_length=50, blank=True, default="")  # 分類
    description = models.TextField(blank=True, default="")  # 描述
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # 身高
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # 體重
    types = models.ManyToManyField(PokemonType)  # 屬性
    time_of_day = models.CharField(max_length=20, choices=TimeOfDay.choices, blank=True, default="")# 能遇見的時間
    weather = models.CharField(max_length=20, choices=Weather.choices, blank=True, default="")# 能遇見的天氣
    # habitats = models.ManyToManyField(blank=True, default=list)  # 可出現的棲地
    specialties = models.ManyToManyField(
        blank=True, default=list
    )  # 專長
    preferred_environment = models.CharField(
        max_length=20, choices=Habitat.choices, blank=True, default=""
    )  # 喜歡的環境
    favorites = models.ManyToManyField(  # 喜歡的東西
        "Item", blank=True, related_name="favored_by_pokemon"
    )
    flavor = models.CharField(
        max_length=20, choices=Flavor.choices, blank=True, default=""
    )
    is_unique_npc = models.BooleanField(default=False)  # 是否為特殊 NPC 寶可夢
    is_event = models.BooleanField(default=False)  # 是否為活動限定寶可夢
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.default_form_name:
            return f"{self.default_name} ({self.default_form_name})"
        return self.default_name

    # def get_translation(self, language_code):
    #     return self.translations.filter(language_code=language_code).first()

    # def display_name(self, language_code=GameLanguage.ENGLISH):
    #     translation = self.get_translation(language_code)
    #     if not translation:
    #         return str(self)
    #     if translation.form_name:
    #         return f"{translation.name} ({translation.form_name})"
    #     return translation.name


class PokemonTranslation(models.Model):
    pokemon = models.ForeignKey(  # 對應的寶可夢主資料
        Pokemon, on_delete=models.CASCADE, related_name="translations"
    )
    language_code = models.CharField(
        max_length=10, choices=GameLanguage.choices
    )  # 這筆翻譯的語系代碼
    name = models.CharField(max_length=100)  # 此語系的寶可夢名稱
    classification = models.CharField(
        max_length=30, blank=True, default=""
    )  # 此語系的分類
    description = models.TextField(blank=True, default="")  # 此語系的描述
    # 喜歡的環境
    specialties = models.ManyToManyField(
        blank=True, default=list
    )  # 此語系的可協助玩家的專長或工作
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(auto_now=True)  # 最後更新時間

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["pokemon", "language_code"],
                name="unique_pokemon_translation_language",
            )
        ]
        indexes = [
            models.Index(fields=["language_code", "name"]),
        ]
        ordering = ["pokemon", "language_code"]

    def __str__(self):
        if self.form_name:
            return f"{self.name} ({self.form_name}) [{self.language_code}]"
        return f"{self.name} [{self.language_code}]"



class PokemonRegion(models.TextChoices):
    WITHERED_WASTELANDS = "WW", "Withered Wastelands"
    BLEAK_BEACH = "BB", "Bleak Beach"
    ROCKY_RIDGES = "RR", "Rocky Ridges"
    SPARKLING_SKYLANDS = "SS", "Sparkling Skylands"
    PALETTE_TOWN = "PT", "Palette Town"
    CLOUD_ISLAND = "CI", "Cloud Island"
    DREAM_ISLANDS = "DI", "Dream Islands"
    STORY = "ST", "Story"
    EVENT = "EV", "Event"


class ItemCategory(models.TextChoices):
    MATERIAL = "material", "Material"
    FOOD = "food", "Food"
    FURNITURE = "furniture", "Furniture"
    MISC = "misc", "Misc."
    OUTDOOR = "outdoor", "Outdoor"
    UTILITY = "utility", "Utility"
    NATURE = "nature", "Nature"
    BUILDING = "building", "Building"
    BLOCK = "block", "Block"
    KIT = "kit", "Kit"
    KEY_ITEM = "key_item", "Key Item"
    LOST_RELIC_L = "lost_relic_l", "Lost Relic (L)"
    LOST_RELIC_S = "lost_relic_s", "Lost Relic (S)"
    FOSSIL = "fossil", "Fossil"
    OTHER = "other", "Other"


class ColorCustomization(models.TextChoices):
    NONE = "none", "No change possible"
    PAINT = "paint", "Paint"
    PATTERN = "pattern", "Pattern"
    PATTERN_PAINT = "pattern_paint", "Pattern and Paint"




# item (物品、家具、裝飾、...的總稱)
class Item(models.Model):
    slug = models.SlugField(
        max_length=160, unique=True
    )  # 穩定識別用代稱，適合網址、匯入資料或程式查找
    default_name = models.CharField(
        max_length=150
    )  # 預設顯示名稱，通常用英文或主要匯入來源語言
    category = models.CharField(  # 物品分類，例如素材、食物、家具、建築套件
        max_length=20, choices=ItemCategory.choices, default=ItemCategory.OTHER
    )
    locations = models.JSONField(blank=True, default=list)  # 可取得地點清單
    acquisition_methods = models.JSONField(
        blank=True, default=list
    )  # 取得方式清單，例如採集、商店、交換、配方製作
    recipe_materials = models.JSONField(
        blank=True, default=list
    )  # 製作配方需要的素材與數量
    flags = models.JSONField(
        blank=True, default=list
    )  # 家具標籤，例如 Relaxation、Decoration、Toy
    color_customization = models.CharField(  # 是否可改色或改圖案
        max_length=20,
        choices=ColorCustomization.choices,
        default=ColorCustomization.NONE,
    )
    is_craftable = models.BooleanField(default=False)  # 是否可透過配方製作
    is_collectible = models.BooleanField(default=True)  # 是否會登錄到收藏或圖鑑
    source_url = models.URLField(blank=True, default="")  # 資料來源網址
    internal_notes = models.TextField(
        blank=True, default=""
    )  # 內部整理備註，不作為多語系顯示文字
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(auto_now=True)  # 最後更新時間

    class Meta:
        ordering = ["category", "default_name"]

    def __str__(self):
        return self.default_name

    def get_translation(self, language_code):
        return self.translations.filter(language_code=language_code).first()

    def display_name(self, language_code=GameLanguage.ENGLISH):
        translation = self.get_translation(language_code)
        if not translation:
            return self.default_name
        return translation.name


class ItemTranslation(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="translations"
    )  # 對應的物品主資料
    language_code = models.CharField(
        max_length=10, choices=GameLanguage.choices
    )  # 這筆翻譯的語系代碼
    name = models.CharField(max_length=150)  # 此語系的物品名稱
    tag = models.CharField(
        max_length=50, blank=True, default=""
    )  # 此語系的物品標籤或短分類名稱
    description = models.TextField(blank=True, default="")  # 此語系的物品描述
    notes = models.TextField(blank=True, default="")  # 此語系要顯示給使用者看的備註
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(auto_now=True)  # 最後更新時間

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["item", "language_code"],
                name="unique_item_translation_language",
            )
        ]
        indexes = [
            models.Index(fields=["language_code", "name"]),
        ]
        ordering = ["item", "language_code"]

    def __str__(self):
        return f"{self.name} [{self.language_code}]"
