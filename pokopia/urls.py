from django.urls import path

from . import views


app_name = "pokopia"

urlpatterns = [
    # 輸入寶可夢，回傳配對喜好的家具組合
    path("", views.MatchFavoriteItemsView.as_view(), name="match_favorite_items"),
]