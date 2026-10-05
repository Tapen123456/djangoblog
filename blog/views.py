from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Category
from .forms import PostForm


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


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_details.html', {'post': post})


def about(request):
    return render(request, "blog/about.html", {"title": "This is the DjangoBlog About page"})


def base(request):
    return render(request, "blog/base.html", {"title": "This is the DjangoBlog Base page"})


def contact(request):
    return render(request, "blog/contact.html", {"title": "This is the DjangoBlog Contact page"})


class PostCreateView(CreateView):
    model = Post
    fields = ["title", "content", "category", "tags", "status"]
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostUpdateView(UpdateView):
    model = Post
    fields = ["title", "content", "category", "tags", "status"]
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("home")
    from .forms import PostForm

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})