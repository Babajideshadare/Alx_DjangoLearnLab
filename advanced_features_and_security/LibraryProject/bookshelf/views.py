from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

# These require custom permissions defined on Book:
# bookshelf.can_view, bookshelf.can_create, bookshelf.can_edit, bookshelf.can_delete

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    return HttpResponse("Book list - access granted (you have 'can_view').")

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    return HttpResponse("Book create - access granted (you have 'can_create').")

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    return HttpResponse(f"Book edit {pk} - access granted (you have 'can_edit').")

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    return HttpResponse(f"Book delete {pk} - access granted (you have 'can_delete').")