from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


def register(request):
    return render(request, 'blog/register.html')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})