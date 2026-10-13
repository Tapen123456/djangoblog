from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post, Category
from .forms import PostForm, RegisterForm


def home(request):
    posts_list = Post.objects.all().order_by('-id')
    categories = Category.objects.all()

    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Hello Djangoblog',
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'blog/post_list.html', context)


# Part D: draft visibility fix
def post_detail(request, slug):
    posts = Post.objects.filter(status="published")
    if request.user.is_authenticated:
        posts = Post.objects.filter(
            Q(status="published") | Q(author=request.user)
        )
    post = get_object_or_404(posts, slug=slug)
    return render(request, 'blog/post_details.html', {'post': post})


def about(request):
    return render(request, "blog/about.html", {"title": "This is the DjangoBlog About page"})


def base(request):
    return render(request, "blog/base.html", {"title": "This is the DjangoBlog Base page"})


def contact(request):
    return render(request, "blog/contact.html", {"title": "This is the DjangoBlog Contact page"})


# Part A: custom 403 page
def custom_403(request, exception=None):
    return render(request, "blog/403.html", status=403)


# Part B: flash messages added to create / update / delete
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post published successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    login_url = "login"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Post deleted.")
        return super().form_valid(form)


class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/my_post.html"
    paginate_by = 6
    login_url = "login"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by("-created_at")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response