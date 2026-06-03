from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Favorite, Habitat, Item, Pokemon


class NamedLookupAdminForm(forms.ModelForm):
    pokemons = forms.ModelMultipleChoiceField(
        label="對應寶可夢",
        queryset=Pokemon.objects.order_by("dex_number", "name_zh_hant"),
        required=False,
        widget=FilteredSelectMultiple("寶可夢", is_stacked=False),
    )

    class Meta:
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["pokemons"].initial = self.instance.pokemon_set.all()


@admin.register(Favorite)
class NamedLookupAdmin(admin.ModelAdmin):
    form = NamedLookupAdminForm
    list_display = ("name_zh_hant", "related_pokemons")
    search_fields = ("name_zh_hant", "pokemon__name_zh_hant")
    readonly_fields = ("related_pokemons",)
    ordering = ("name_zh_hant",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("pokemon_set")

    @admin.display(description="對應寶可夢")
    def related_pokemons(self, obj):
        return ", ".join(pokemon.name_zh_hant for pokemon in obj.pokemon_set.all())

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.pokemon_set.set(form.cleaned_data["pokemons"])




@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = (
        "dex_number",
        "name_zh_hant",
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
        "specialties",
        "favorites",
    )
    search_fields = (
        "name_zh_hant",
        "favorites__name_zh_hant",
    )
    filter_horizontal = ("types", "habitats", "specialties", "favorites")
    ordering = ("dex_number", "name_zh_hant")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name_zh_hant", "category", "tag")
    list_filter = ("tag", "category", "favorites")
    search_fields = ("name_zh_hant", "favorites__name_zh_hant")
    filter_horizontal = ("favorites",)
    ordering = ("category", "name_zh_hant")
