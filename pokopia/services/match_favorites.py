from itertools import product

from pokopia.models import Item, ItemTag, Pokemon


def match_favorite_items(pokemon_number):
    if not pokemon_number:
        return []

    pokemon = (
        Pokemon.objects.prefetch_related("favorites")
        .filter(dex_number=pokemon_number)
        .first()
    )
    if pokemon is None:
        return []

    pokemon_favorite_names = {favorite.name for favorite in pokemon.favorites.all()}
    rest_tag = ItemTag.REST.value
    decoration_tag = ItemTag.DECORATION.value
    toy_tag = ItemTag.TOY.value
    target_tags = (rest_tag, decoration_tag, toy_tag)
    items = (
        Item.objects.prefetch_related("favorites")
        .filter(tag__in=target_tags, favorites__name__in=pokemon_favorite_names)
        .distinct()
    )

    items_by_tag = {tag: [] for tag in target_tags}
    item_favorites = {}
    for item in items:
        items_by_tag[item.tag].append(item)
        item_favorites[item.pk] = {
            favorite.name for favorite in item.favorites.all()
        } & pokemon_favorite_names

    matched_groups = []
    for rest_item, decoration_item, toy_item in product(
        items_by_tag[rest_tag],
        items_by_tag[decoration_tag],
        items_by_tag[toy_tag],
    ):
        matched_favorites = (
            item_favorites[rest_item.pk]
            | item_favorites[decoration_item.pk]
            | item_favorites[toy_item.pk]
        )
        if len(matched_favorites) >= 4:
            matched_groups.append((rest_item, decoration_item, toy_item))

    return matched_groups