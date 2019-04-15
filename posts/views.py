from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Image, Comment
from .forms import PostForm, ImageForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def list(request):
    posts = Post.objects.all()
    images = Image.objects.all()
    context = {'posts': posts, 'images': images}
    return render(request, 'posts/list.html', context)

@login_required
def new(request):
    if request.method == "POST":
        # post = Post()
        # post.content = request.POST.get('content')
        # post.save()
        post_form = PostForm(request.POST, request.FILES)
        image_form = ImageForm(request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            files = request.FILES.getlist('file')
            for file in files:
                request.FILES['file'] = file
                image_form = ImageForm(request.POST, request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect(post)
    else:
        post_form = PostForm()
        image_form = ImageForm()
    context = {'post_form': post_form, 'image_form': image_form}
    return render(request, 'posts/form.html', context)

def detail(request, post_pk):
    # Post.objects.get(pk=post_pk)
    post = get_object_or_404(Post, pk=post_pk)
    context = {'post': post}
    return render(request, 'posts/detail.html', context)
    
def edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES, instance=post)
        image_form = ImageForm(request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            files = request.FILES.getlist('file')
            for file in files:
                request.FILES['file'] = file
                image_form = ImageForm(request.POST, request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect(post)
    else:
        post_form = PostForm(instance=post)
        image_form = ImageForm()
    context = {'post_form':post_form, 'image_form':image_form}
    return render(request, 'posts/form.html', context)
    
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method=="POST":
        post.delete()
    return redirect('posts:list')
        
def new_comment(request, post_pk):
    if request.method == "POST":
        comments = Comment()
        comments = request.POST.comments
        comments.save()
        context = {'comments':comments}
        return redirect('posts:detail', post_pk)
        
        
# def new_comment(request, post_pk):
#     if request.method == "POST":
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             comment_form.save()
#             return redirect('posts:detail', post_pk)
#     else:
#         comment_form = CommentForm()
#     context = {'comment_form':comment_form}
#     return render(request, 'detail.html', context)