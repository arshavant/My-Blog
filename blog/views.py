from django.shortcuts import render, redirect
from django.views import View
from .forms import CommentForm
from .models import Post, Comment
from accounts.models import Account


# Create your views here.


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-date')

        is_logged_in = request.session.get('is_logged_in')
        user_id = request.session.get('logged_account_id')

        try:
            account = Account.objects.get(pk=user_id)

            return render(request, 'blog/home.html', {
                'posts': posts,
                'is_logged_in': is_logged_in,
                'account': account,
            })
        except Account.DoesNotExist:
            request.session['is_logged_in'] = False

            return render(request, 'blog/home.html', {
                'posts': posts,
                'is_logged_in': is_logged_in,
            })


class SinglePostView(View):
    def get(self, request, slug):
        post = Post.objects.all().get(slug=slug)
        comments = Comment.objects.filter(post=post)

        comment_form = CommentForm()

        is_logged_in = request.session.get('is_logged_in')

        return render(request, "blog/single-post.html", {
            'post': post,
            'comment_form': comment_form,
            'comments': comments,
            'is_logged_in': is_logged_in,
        })

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)

        comment_form = CommentForm(request.POST)

        user_id = request.session.get('logged_account_id')

        try:
            if comment_form.is_valid():
                new_comment = Comment(
                    author=Account.objects.get(pk=user_id),
                    post=post,
                    text=comment_form.cleaned_data['text'],
                    rating=comment_form.cleaned_data['rating'],
                )

                new_comment.save()
                return redirect('single_post', slug=slug)
        except Account.DoesNotExist:
            request.session['is_logged_in'] = False
            return redirect('home')



