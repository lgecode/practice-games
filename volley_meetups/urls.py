from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    # path("form/new", views.CampFormCreateView.as_view(), name="new_form"),
]
