from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from django.urls import reverse_lazy

import stripe
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

stripe.api_key = "PUT YOUR STRIPE SECRET KEY also put public key on blog/post_form.html"

from .forms import CommentForm, post_create
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


def home(request):
    abc = Post.objects.order_by('-date_posted')
    context = {
        'posts': Post.objects.all(),
        'abc': abc

    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# also add Comment view
class PostDetailView(DetailView):
    model = Post


# class based view

# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title', 'content']
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


# function based view with stripe payment

def post_create1(request):
    if request.method == 'POST':
        form = post_create(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            try:
                amount = int(request.POST['amount'])
                customer = stripe.Customer.create(
                    email=request.POST['email'],
                    name=request.POST['nickname'],
                    source=request.POST['stripeToken'],
                    address={
                        'line1': '510 Townsend St',
                        'postal_code': '98140',
                        'city': 'San Francisco',
                        'state': 'CA',
                        'country': 'US',
                    },

                )

                charge = stripe.Charge.create(
                    customer=customer,
                    amount=amount * 100,
                    currency='usd',
                    description="donation"

                )

                user.save()
                return redirect('blog-home')

            except:
                HttpResponse('form is invalid')

    else:
        form = post_create()

    return render(request, 'blog/post_form.html', {'form': form})


# simple function based view

# def post_create1(request):
#     if request.method == 'POST':
#         form = post_create(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.author = request.user
#             user.save()
#             return redirect('/')
#     else:
#         form = post_create()
#
#     return render(request, 'blog/post_form.html', {'form': form})


class AddCommentView(CreateView):
    model = Comment
    template_name = 'blog/add_comment.html'
    form_class = CommentForm
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
