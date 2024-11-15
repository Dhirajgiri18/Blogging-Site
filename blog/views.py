from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from .models import PostModel, Like
from .forms import PostModelForm, PostUpdateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


@login_required
def index(request):
    posts = PostModel.objects.all()
    
    # Check if the user has liked each post
    for post in posts:
        post.is_liked = Like.objects.filter(user=request.user, post=post).exists()
        post.like_count = post.like_count()
        

    if request.method == 'POST':
        # Handle Post creation
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('blog-index')
        
        # Handle "Like" action
        if 'like' in request.POST:
            post_id = request.POST.get('post_id')
            post = PostModel.objects.get(id=post_id)
            if not Like.objects.filter(user=request.user, post=post).exists():
                Like.objects.create(user=request.user, post=post)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect to the same page

    else:
        form = PostModelForm()

    context = {
        'posts': posts,
        'form': form
    }

    return render(request, 'blog/index.html', context)





@login_required
def post_detail(request, pk):
    try:
        post = PostModel.objects.get(id=pk)
    except PostModel.DoesNotExist:
        raise Http404("Post not found")
    
    is_liked = Like.objects.filter(user=request.user, post=post).exists()

    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('blog-post-detail', pk=post.id)

        # Handling "like" action
        if 'like' in request.POST and not is_liked:
            Like.objects.create(user=request.user, post=post)
            return redirect('blog-post-detail', pk=post.id)

    else:
        c_form = CommentForm()

    context = {
        'post': post,
        'c_form': c_form,
        'is_liked': is_liked,  # Pass the like status
    }

    return render(request, 'blog/post_detail.html', context)


@login_required
def post_edit(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog-post-detail', pk=post.id)
    else:
        form = PostUpdateForm(instance=post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/post_edit.html', context)


@login_required
def post_delete(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog-index')
    context = {
        'post': post
    }
    return render(request, 'blog/post_delete.html', context)


class CustomLogoutView(LogoutView):
    # Override get_redirect_url to specify your custom URL
    def get_redirect_url(self):
        return reverse_lazy('users-logout-success')  # Replace with the URL pattern of your choice