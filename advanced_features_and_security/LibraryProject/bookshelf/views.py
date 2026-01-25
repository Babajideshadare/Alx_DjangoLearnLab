from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_protect

from .models import Book
from .forms import ExampleForm
from .forms import BookSearchForm

# Secure search using Django forms + ORM (prevents SQL injection)
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()
    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            books = books.filter(title__icontains=q)
    context = {"form": form, "books": books}
    return render(request, "bookshelf/book_list.html", context)

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    return HttpResponse("Book create - access granted (you have 'can_create').")

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    return HttpResponse(f"Book edit {pk} - access granted (you have 'can_edit').")

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    return HttpResponse(f"Book delete {pk} - access granted (you have 'can_delete').")

# CSRF-protected POST form using Django forms (safe input handling)
@csrf_protect
def form_example(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            return render(request, "bookshelf/form_example.html", {"form": ExampleForm(), "submitted_name": name})
    else:
        form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})