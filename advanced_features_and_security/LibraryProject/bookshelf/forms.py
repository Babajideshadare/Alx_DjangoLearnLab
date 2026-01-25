from django import forms

class BookSearchForm(forms.Form):
    q = forms.CharField(
        label="Search",
        required=False,
        max_length=100,
        strip=True,
    )

class ExampleForm(forms.Form):
    name = forms.CharField(
        label="Name",
        min_length=2,
        max_length=50,
        strip=True,
    )