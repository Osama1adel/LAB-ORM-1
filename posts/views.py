from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Post
from .forms import PostForm, SearchForm


def home(request):
    posts = Post.objects.filter(is_published=True).order_by("-published_at")
    return render(request, "posts/home.html", {"posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "posts/detail.html", {"post": post})


def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "posts/add_post.html", {"form": form})


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, "posts/edit_post.html", {"form": form, "post": post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("home")
    return render(request, "posts/delete_post.html", {"post": post})


def search(request):
    form = SearchForm(request.GET or None)
    qs = Post.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get("q")
        category = form.cleaned_data.get("category")
        is_published = form.cleaned_data.get("is_published")
        order = form.cleaned_data.get("order") or "-published_at"
        per_page = form.cleaned_data.get("per_page") or 10

        # Filtering
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))

        if category:
            qs = qs.filter(category=category)

        if is_published is True:
            qs = qs.filter(is_published=True)
        elif is_published is False:
            qs = qs.filter(is_published=False)

        # Ordering (مع whitelist بسيطة للأمان)
        allowed = {"-published_at", "published_at", "title", "-title"}
        if order not in allowed:
            order = "-published_at"
        qs = qs.order_by(order)

        # Limiting / Pagination
        paginator = Paginator(qs, per_page)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "form": form,
            "page_obj": page_obj,
            "total": qs.count(),
            "order": order,
        }
        return render(request, "posts/search.html", context)

    # أول تحميل للصفحة بدون مدخلات
    paginator = Paginator(qs.order_by("-published_at"), 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "posts/search.html",
        {"form": form, "page_obj": page_obj, "total": qs.count()},
    )
