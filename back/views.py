from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    user = request.user
    print(user)
    return render(
        request,
        "back/index.html",
        { "user": user }
    )

@login_required
def profile(request):
    user = request.user
    return render(
        request,
        "back/profile.html",
        { "user": user },
    )