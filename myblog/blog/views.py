from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
from .models import Post,Category, Comment
from .forms import PostForm, CommentForm
from django.db.models import Count
from django.contrib import messages

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    query_string = request.GET.get('category')
    if query_string:
        posts = Post.objects.filter(published_date__lte=timezone.now(), category__name=query_string).order_by('published_date')

    if posts.count() < 1:
        messages.error(request, f'No post in {query_string} category found')
    categories = Category.objects.annotate(count_post=Count('post'))
    context = {
        'posts' : posts,
        'categories' : categories
    }
    return render(request, 'blog/post_list.html', {'context': context})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post_id=pk).order_by('id')

    query_string = request.GET.get('comment_id')
    if query_string:
        comment = get_object_or_404(Comment, pk=query_string)
        comment_form = CommentForm(instance=comment)
        if request.method == "POST":
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('blog:post_detail', pk=post.pk)

    else:
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.comentator = request.user
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
            messages.success(request, 'New Post Added')
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
            messages.success(request, 'This Post Edited ')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
    delete = Post.objects.get(id=pk).delete()
    messages.success(request, 'Post Deleted')
    return redirect('blog:post_list')

def comment_delete(request, post_id, pk):
    delete = Comment.objects.get(id=pk).delete()
    messages.success(request, 'Comment Deleted')
    return redirect('blog:post_detail', pk=post_id)