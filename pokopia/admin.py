import os

from django.conf import settings
from django.contrib import admin

from .models import Favorite, Habitat, Item, Pokemon, PokemonType, Specialty


ITEM_IMAGE_DIR = settings.BASE_DIR / "pokopia" / "static" / "pokopia" / "images" / "items"


def item_image_exists(obj):
    return bool(obj.slug) and os.path.exists(ITEM_IMAGE_DIR / f"{obj.slug}.png")


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("name_zh_hant",)
    ordering = ("name_zh_hant",)


@admin.register(Habitat)
class HabitatAdmin(admin.ModelAdmin):
    list_display = ("number", "name_zh_hant", "is_event")
    list_display_links = ("number", "name_zh_hant",)
    list_filter = ("is_event",)
    ordering = ("is_event", "number")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("name_zh_hant",)
    ordering = ("name_zh_hant",)


@admin.register(PokemonType)
class PokemonTypeAdmin(admin.ModelAdmin):
    list_display = ("name_zh_hant",)
    ordering = ("name_zh_hant",)


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = (
        "dex_number",
        "name_zh_hant",
        "specialties_display",
        "is_event",
        "is_unique_npc",
    )
    list_display_links = ("dex_number", "name_zh_hant",)
    list_filter = (
        "is_event",
        "specialties",
        "types",
        "is_unique_npc",
        "preferred_environment",
        "flavor",
        "favorites",
    )
    search_fields = (
        "name_zh_hant",
        "favorites__name_zh_hant",
    )
    filter_horizontal = ("types", "habitats", "specialties", "favorites")
    ordering = ("is_event", "dex_number", "name_zh_hant")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("specialties")

    @admin.display(description="專長")
    def specialties_display(self, obj):
        return ", ".join(specialty.name_zh_hant for specialty in obj.specialties.all())


class HasImageListFilter(admin.SimpleListFilter):
    title = "has image"
    parameter_name = "has_image"

    def lookups(self, request, model_admin):
        return (
            ("1", "yes"),
            ("0", "no"),
        )

    def queryset(self, request, queryset):
        has_image = self.value()
        if has_image not in ("1", "0"):
            return queryset

        matched_item_ids = [
            obj.pk
            for obj in queryset.only("pk", "slug")
            if item_image_exists(obj) == (has_image == "1")
        ]
        return queryset.filter(pk__in=matched_item_ids)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name_zh_hant", "category", "tag", "has_image")
    list_filter = (HasImageListFilter, "tag", "category", "favorites")
    search_fields = ("name_zh_hant",)
    filter_horizontal = ("favorites",)
    ordering = ("category", "name_zh_hant")

    @admin.display(description="has image", boolean=True)
    def has_image(self, obj):
        return item_image_exists(obj)