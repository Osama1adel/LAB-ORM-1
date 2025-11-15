from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

def home(request):
    posts = Post.objects.filter(is_published=True).order_by("-published_at")
    return render(request, "posts/home.html", {"posts": posts})

def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "posts/add_post.html", {"form": form})
