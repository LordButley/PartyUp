from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth import get_user
from .models import Post, Game, Comment
from .forms import PostForm, CommentForm


# Create your views here.

class GameList(generic.ListView):
    model = Game
    template_name = 'index.html'

class GamePostList(View):

    def get(self, request, ref_name):
        game_obj= Game.objects.get(ref_name=ref_name)

        post = Post.objects.filter(game=game_obj)

        return render(request, 'game_page.html',
            {
                "post": post,
                "game": game_obj
            },
        )

class GameComment(View):

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        game_obj = Game.objects.get(post=post)

        comments = Comment.objects.filter(post=post)

        return render(request, 'post_page.html',
            {
              "post": post,
              "game": game_obj,
              "comments": comments,
              "comment_form": CommentForm()
            }
      
    )

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        comments = Comment.objects.filter(post=post)

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.author = get_user(request)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(request, 'post_page.html',
            {
              "post": post,
              "comments": comments,
              "comment_form": CommentForm()
            }
      
    )


class CreatePost(View):

    def get(self, request, ref_name):
        game_obj= Game.objects.get(ref_name=ref_name)
        return render(request, 'create_post.html',
        {
            "post_form": PostForm(),
            "game": game_obj
        }
        )

    def post(self, request, ref_name):
        game_obj= Game.objects.get(ref_name=ref_name)

        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            post_form.instance.name = request.user.username
            post = post_form.save(commit=False)
            post.author = get_user(request)
            post.game = Game.objects.get(ref_name=ref_name)
            post.save()
            # return HttpResponseRedirect('game_page' 'ref_name')
            url = request.POST.get("url")
            messages.success(request, "Post created! You're one step closer to Partying Up!")
            return redirect(reverse("game_page", args=(url,)))
        else:
            post_form = PostForm()

        return render(request, 'create_post.html',
        {
            "post_form": PostForm()
        }
        )

class EditPost(View):

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        if post.author.id == request.user.id:
            game_obj = post.game
            return render(request, 'edit_post.html',
            {
                "post_form": PostForm(instance=post),
                "post": post,
                "game": game_obj
            }
            )
        return render(request, "403.html")

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        game_obj = post.game

        post_form = PostForm(data=request.POST, instance=post)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.save()
            url = request.POST.get("url")
            messages.success(request, "Post updated :)")
            return redirect(reverse("game_page", args=(url,)))
        else:
            post_form = PostForm()

        return render(request, 'edit_post.html',
        {
            "post_form": PostForm()
        }
        )

def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author.id == request.user.id:
        game_obj = post.game
        url = game_obj.ref_name
        post.delete()
        messages.success(request, "Post deleted! Feel free to post a new one")
        return redirect(reverse("game_page", args=(url,)))
    return render(request, '403.html')

def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if comment.author.id == request.user.id:
        comment.delete()
        # return redirect(reverse("post_page"), args=(comment.post.id))
        url = comment.post.id
        print(url)
        messages.success(request, "Comment deleted! Feel free to post a new one")
        return redirect(reverse("post_page", args=(url,)))

    return render(request, '403.html')
