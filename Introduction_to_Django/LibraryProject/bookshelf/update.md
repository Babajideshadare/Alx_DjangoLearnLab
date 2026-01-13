b = Book.objects.get(title="1984")
b.title = "Nineteen Eighty-Four"
b.save()
(b.id, b.title, b.author, b.publication_year)
# Output: (1, 'Nineteen Eighty-Four', 'George Orwell', 1949)
