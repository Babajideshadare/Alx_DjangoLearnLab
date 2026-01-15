from django.contrib import admin

# Register your models here.
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')   # show these columns
    list_filter = ('author', 'publication_year')             # filter sidebar
    search_fields = ('title', 'author')                      # search box

admin.site.register(Book, BookAdmin)