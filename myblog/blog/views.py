from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
from .models import Post,Category, Comment
from .forms import PostForm, CommentForm

# Create your views here.
def post_list(request):

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    categories = Category.objects.all()
    context = {
        'posts' : posts,
        'categories' : categories
    }
    return render(request, 'blog/post_list.html', {'context': context})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post_id=pk).order_by('id')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_id = pk
            post.save()
            return redirect('blog:post_detail', pk=pk)
    else:
        comment_form = CommentForm()
    context = {
        'post' : post,
        'comments' : comments,
        'comment_form' : comment_form
    }
    return render(request, 'blog/post_detail.html', {'context': context})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
    delete = Post.objects.filter(id=pk).delete()
    return redirect('blog:post_list')