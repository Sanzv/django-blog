from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


# Create your views here.


def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/blog.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    #   Making the current or the requesting user the author of the post being created by Overriding form_valid() method
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_save(self, form):
        form.instance.author = self.request.user
        return super().form_save(form)

    # Allows only the author of the post to update thee post By overriding the test_func() method
    def test_func(self):
        # Get the current instance of the post that is being updated
        post = self.get_object()

        # Check to see if the author and the current user matches
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    # Allows only the author of the post to update thee post By overriding the test_func() method
    def test_func(self):
        # Get the current instance of the post that is being updated
        post = self.get_object()

        # Check to see if the author and the current user matches
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'about'})
