from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm

def list(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'posts/list.html', context)
    
def edit(request, post_pk):
    post = get_object_or_404(Post, post_pk)
    if request.method == "POST":
        post_form = PostForm(request.POST, instance = post)
        if post_form.is_valid():
            # post = Post()
            # post.title = request.POST.get('title')
            # post.content = request.POST.get('content')
            # post.save()
            post = post_form.save(commit = False) # commit=False로 잠깐 멈추는 이유는 위처럼 무식하게 짤 때는
            post.user = request.user              # save위에 넣어주면 되는데 폼으로는 한번에 저장이 되므로
            post.save()                           # 잠깐 멈춰준다.
            return redirect('posts:detail', post_pk)
    else:
        post_form = PostForm(instance = post)
    context = {'post_form': post_form}
    return render(request, 'edit.html', context)