from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from post_app.models import Post, Vote
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from secrets import compare_digest


def main_page(request):
    all_posts = Post.objects.all()
    context = {
        "all_posts": all_posts,
    }
    return render(request, 'index.html', context)


def post_detail_page(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        "post": post,
    }
    return render(request, 'post.html', context)


@login_required
def user_detail_page(request, user_id):
    all_posts = Post.objects.all()
    posts_count = all_posts.count()
    user = User.objects.get(pk=user_id)
    context = {
        "user": user,
        "written_posts": posts_count,
    }
    return render(request, 'user.html', context)


def signup(request):
    if request.method == 'POST':
        data = request.POST

        password = data['formPassword']
        password_repeat = data['formPasswordRepeat']
        username = data['formUsername']

        if compare_digest(password, password_repeat) and username is not None:
            params = {
                'password': password,
                'username': username,
            }
            new_user = User.objects.create_user(**params)
            login(request, new_user)
            return redirect('main')

    return render(request, 'registration/signup.html')


@login_required
def write_page(request):
    return render(request, 'write.html', {})


@login_required
def post_to_db(request):

    if request.method == 'POST':
        article_title = request.POST.get('article_name', '')
        article_text = request.POST.get('article_text', '')

        article = Post(
            author=request.user,
            title=article_title,
            content=article_text,
        )
        article.save()

    return redirect('main')


@login_required
def rate_post(request, post_id):
    current_user = request.user
    post = get_object_or_404(Post, pk=post_id)
    rate = request.POST['like']
    voted_users = post.voters.all()

    # for user in voted_users:
    #     vote = Vote.objects.get(user=user, post=post)
    #     print("!!! {}: {}".format(user, vote.choice))

    if current_user in voted_users:
        vote = Vote.objects.get(user=current_user, post=post_id)
        
        if rate == 'like' and vote.choice == 'like':
            print(rate, vote.choice)
            pass
        elif rate == 'dislike' and vote.choice == 'dislike':
            print(rate, vote.choice)
            pass
        elif rate == 'like' and vote.choice == 'dislike':
            print(rate, vote.choice)
            post.dislikes -= 1
            post.likes += 1
            vote.choice = 'like'
        else:
            print(rate, vote.choice)
            post.dislikes += 1
            post.likes -= 1
            vote.choice = 'dislike'
        vote.save()
    else:
        post.voters.add(current_user)
        vote = Vote.objects.get(user=current_user, post=post_id)
        if rate == 'like':
            post.likes += 1
            vote.choice = 'like'
        else:
            post.dislikes += 1
            vote.choice = 'dislike'
    post.save()
    # return JsonResponse({
    #         'message': 'Vote successfully updated!',
    #         'likes_count': post.likes,
    #         'dislikes_count': post.dislikes
    #     })
    return redirect('main')