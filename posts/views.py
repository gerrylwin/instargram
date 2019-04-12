from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
# Create your views here.
def list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'posts/list.html', context)

def new(request):
    if request.method == "POST":
        # post = Post()
        # post.content = request.POST.get('content')
        # post.save()
        form = PostForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('posts:list')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'posts/new.html', context)

def detail(request, post_pk):
    # Post.objects.get(pk=post_pk)
    post = get_object_or_404(Post, pk=post_pk)
    context = {'post': post}
    return render(request, 'posts/detail.html', context)
    
def edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('posts:list')
    else:
        form = PostForm(instance=post)
    context = {'form':form}
    return render(request, 'posts/edit.html', context)
    
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method=="POST":
        post.delete()
    return redirect('posts:list')
        
    