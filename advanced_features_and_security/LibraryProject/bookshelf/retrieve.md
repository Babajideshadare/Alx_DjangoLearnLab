b = Book.objects.get(title="1984")
(b.id, b.title, b.author, b.publication_year)
# Output: (1, '1984', 'George Orwell', 1949)