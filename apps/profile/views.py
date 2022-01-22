from django.shortcuts import render, redirect

from .forms import ProfileForm


def login(request):
    return render(request, 'profile/login.html')


def profile(request):
    if (request.method == 'POST'):
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile:main')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile/main.html', {'form': form})
