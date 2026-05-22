from django.contrib import admin

from .models import Favorite, Habitat, Item, Pokemon, PokemonType, Specialty


@admin.register(PokemonType, Habitat, Specialty, Favorite)
class NamedLookupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = (
        "pokopia_dex_number",
        "name",
        "classification",
        "preferred_environment",
        "flavor",
        "is_unique_npc",
        "is_event",
    )
    list_filter = (
        "preferred_environment",
        "flavor",
        "is_unique_npc",
        "is_event",
        "types",
        "habitats",
        "specialties",
        "favorites",
    )
    search_fields = (
        "name",
        "classification",
        "description",
        "types__name",
        "habitats__name",
        "specialties__name",
        "favorites__name",
    )
    filter_horizontal = ("types", "habitats", "specialties", "favorites")
    ordering = ("pokopia_dex_number", "name")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "tag")
    list_filter = ("category", "tag", "favorites")
    search_fields = ("name", "description", "favorites__name")
    filter_horizontal = ("favorites",)
    ordering = ("category", "name")
