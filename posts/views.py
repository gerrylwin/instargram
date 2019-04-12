from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Image
from .forms import PostForm, ImageForm
# Create your views here.
def list(request):
    posts = Post.objects.all()
    images = Image.objects.all()
    context = {'posts': posts, 'images': images}
    return render(request, 'posts/list.html', context)

def new(request):
    if request.method == "POST":
        # post = Post()
        # post.content = request.POST.get('content')
        # post.save()
        post_form = PostForm(request.POST, request.FILES)
        image_form = ImageForm(request.FILES)
        if post_form.is_valid():
            post = post_form.save()
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
        if post_form.is_valid():
            post = post_form.save()
            return redirect(post)
    else:
        post_form = PostForm(instance=post)
    context = {'post_form':post_form}
    return render(request, 'posts/form.html', context)
    
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method=="POST":
        post.delete()
    return redirect('posts:list')
        
    