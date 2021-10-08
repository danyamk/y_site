from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostForm
from posts.models import Group, Post


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    new_user = get_object_or_404(User, username=username)
    posts_count = new_user.posts.count()
    user_posts = Post.objects.filter(author=new_user)
    paginator = Paginator(user_posts, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {
        'username': new_user,
        'post_count': posts_count,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    username = post.author
    posts_count = username.posts.count()
    context = {
        'post': post,
        'username': username,
        'posts_count': posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
        return render(request, 'posts/create_post.html', {'form': form})
    else:
        form = PostForm()
        return render(request, 'posts/create_post.html', {'form': form})


@login_required()
def post_edit(request, post_id):
    is_edit = False
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(data=request.POST or None, instance=post)
    if post.author == request.user:
        is_edit = True
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('posts:post_edit', post.id)
    return render(request, 'posts/create_post.html',
                 {'form': form, 'is_edit': is_edit})
