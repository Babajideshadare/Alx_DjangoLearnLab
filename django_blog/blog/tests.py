from django.shortcuts import render

def register(request):
    return render(request, 'blog/register.html')

def profile(request):
    return render(request, 'blog/profile.html')