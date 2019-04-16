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
        if request.user != post.user:
            return redirect(post)
        post_form = PostForm(instance=post)
        image_form = ImageForm()
    context = {'post_form':post_form, 'image_form':image_form}
    return render(request, 'posts/form.html', context)
    
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user != post.user:
        return redirect('posts:list')
    if request.method=="POST":
        post.delete()
    return redirect('posts:list')
        
# def new_comment(request, post_pk):
#     if request.method == "POST":
#         comments = Comment()
#         comments = request.POST.comments
#         comments.save()
#         context = {'comments':comments}
#         return redirect('posts:detail', post_pk)

def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {'post': post, 'comment_form':comment_form}
    return render(request, 'posts/detail.html', context)        

def new_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    return redirect('posts:detail', post_pk)

def del_comment(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # comment = Comment.objects.all()
    # if request.user != post.comment.comment.user:
    if request.method == "POST":
        comment = Comment.objects.get(pk=comment_pk)
        post.comment.delete()
    return redirect('posts:detail', post_pk)

def like(request, post_pk): # 어떤 포스트인지 아이디를 가져와야하므로
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user # 로그인 된 유저의 정보를 가져옴
    # user가 지금 해당 게시글에 좋아요를 한적이 있는지 ?
    # if user in post.like_users.all():
    #     post.like_users.remove(user)
    # else:
    #     post.like_users.add(user)
    if post.like_users.filter(pk=user.id).exists():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    return redirect('posts:detail', post.pk)