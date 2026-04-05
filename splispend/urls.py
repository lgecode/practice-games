from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    # path("", views.expense_book_list, name="expense_book_list"),
    path(
        "expense-book/<int:pk>/", views.expense_book_detail, name="expense_book_detail"
    ),
    # path("expense-book/new/", views.expense_book_create, name="expense_book_create"),
    # path("expense-book/<int:pk>/edit/", views.expense_book_update, name="expense_book_update"),
    # path("expense-book/<int:pk>/delete/", views.expense_book_delete, name="expense_book_delete"),
    path(
        "expense-record/new/", views.expense_record_create, name="expense_record_create"
    ),
    path(
        "expense-record/<int:pk>/edit/",
        views.expense_record_update,
        name="expense_record_update",
    ),
    path(
        "expense-record/<int:pk>/delete/",
        views.expense_record_delete,
        name="expense_record_delete",
    ),
]
