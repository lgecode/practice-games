from django.shortcuts import render
from django.shortcuts import redirect
from .models import ExpenseBook, ExpenseRecord


def index(request):
    expense_books = ExpenseBook.objects.all().first()
    if not expense_books:
        expense_books = ExpenseBook.objects.create(name="Default")
    return redirect("expense_book_detail", pk=expense_books.id)
    # return render(request, "index.html")


def expense_book_detail(request, pk):
    expense_book = ExpenseBook.objects.get(id=pk).prefetch_related(
        Prefetch("expense_records", queryset=ExpenseRecord.objects.all())
    )
    return render(request, "expense_book_detail.html", {"expense_book": expense_book})


def expense_record_create(request):
    return render(request, "expense_record_create.html")


def expense_record_update(request):
    return render(request, "expense_record_update.html")


def expense_record_delete(request):
    return render(request, "expense_record_delete.html")
