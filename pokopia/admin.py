from django.contrib import admin

from .models import Favorite, Habitat, Item, Pokemon, PokemonType, Specialty


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


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name_zh_hant", "category", "tag")
    list_filter = ("tag", "category", "favorites")
    search_fields = ("name_zh_hant",)
    filter_horizontal = ("favorites",)
    ordering = ("category", "name_zh_hant")
