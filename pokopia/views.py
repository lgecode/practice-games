import json
from django.http import HttpResponse
from django.views import View
from pokopia.services.match_favorites import match_favorite_items


favorites = {
    '交通工具',
    '可愛的',
    '圓滾滾的',
    '垃圾',
    '堅硬的',
    '色彩繽紛的',
    '大家一起用的',
    '奇妙的',
    '容器',
    '尖尖的',
    '布製的',
    '建設',
    '像食物的',
    '會搖晃的',
    '整潔的',
    '會旋轉的',
    '有文字的',
    '有玻璃的',
    '木製的',
    '柔軟的',
    '觀賞用的',
    '花朵綻放的',
    '艱深難懂的',
    '石製的',
    '方方的',
    '細長的',
    '集聚在一起的',
    '會發出聲響的',
    '能感受土的',
    '能感受大自然的',
    '能感受水的',
    '能感受海的',
    '能感受火的',
    '能感受風的',
    '能治癒傷口的',
    '訓練用的',
    '詭異的',
    '象徵',
    '豪華的',
    '遊戲區',
    '金屬的',
    '閃亮亮的',
    '以電力驅動的',
}


class MatchFavoriteItemsView(View):
    def get(self, request):
        pokemon_number = request.GET.get("pokemon_number") or request.GET.get("pokemon_numbers")
        matched_groups = match_favorite_items(pokemon_number)
        formatted_groups = [
            {
                "relaxation": rest_item.name,
                "decoration": decoration_item.name,
                "toy": toy_item.name,
            }
            for rest_item, decoration_item, toy_item in matched_groups
        ]
        print(formatted_groups)


        return HttpResponse(
            json.dumps(formatted_groups, ensure_ascii=False, indent=2),
            content_type="application/json; charset=utf-8",
        )