from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import PostForm, CommentForm
from .models import Group, Post, User, Follow

NUMBERS_OF_POSTS = 10


def get_page_content(post_list, page_number):
    paginator = Paginator(post_list, NUMBERS_OF_POSTS)
    return paginator.get_page(page_number)


def index(request):
    post_list = Post.objects.all()
    page_obj = get_page_content(post_list, request.GET.get("page"))
    return render(request, "posts/index.html", context={"page_obj": page_obj})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = get_page_content(posts, request.GET.get("page"))
    return render(
        request,
        "posts/group_list.html",
        context={"group": group, "page_obj": page_obj},
    )


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    following = (
        request.user.is_authenticated
        and Follow.objects.filter(user=request.user, author=user).exists()
    )
    page_obj = get_page_content(posts, request.GET.get("page"))
    return render(
        request,
        "posts/profile.html",
        context={
            "author": user,
            "page_obj": page_obj,
            "following": following,
        },
    )


def post_detail(request, post_id):
    form = CommentForm()
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    return render(
        request,
        "posts/post_detail.html",
        context={"post": post, "form": form, "comments": comments},
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            "posts/create_post.html",
            context={"form": form, "is_edit": False},
        )
    form.instance.author = request.user
    form.save()
    return redirect("posts:profile", request.user.username)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if post.author != request.user:
        return redirect("posts:post_detail", post_id)
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post_id)

    return render(
        request,
        "posts/create_post.html",
        context={"form": form, "is_edit": True},
    )


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    page_obj = get_page_content(posts, request.GET.get("page"))
    return render(request, "posts/follow.html", context={"page_obj": page_obj})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect("posts:follow_index")


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("posts:follow_index")
