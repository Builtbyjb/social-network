from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

import datetime

from .models import User, Posts, Following, Liked


def index(request):
    posts = Posts.objects.all().order_by('-id')

    # Paginate the posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(posts) <= 10:
        paginate = False
    else:
        paginate = True

    current_user = request.user.username

    liked_list = []

    liked = list(Liked.objects.filter(username=current_user).values())

    for i in liked:
        liked_list.append(i["post_id"])

    return render(request, "network/index.html",{
        "header": "All Posts",
        "posts": page_obj,
        "paginate": paginate,
        "current_user": current_user,
        "liked": liked_list,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def create_post(request):
    if request.method == "POST":
        now = datetime.datetime.now()
        user = request.user

        Posts(
            username = user.username,
            user_id = user.id,
            post = request.POST["post-text"],
            timestamp = now,
        ).save()

        return JsonResponse({
            "response": "Post Created",
        })

    return render(request, "network/create_post.html", {
        "header": "New Post",
        "inputValue": "Post",
    })

def edit_post(request):
    if request.method == "POST":
        id = request.POST["id"]
        post_text = request.POST["post-text"]

        post = Posts.objects.get(id=id)
        post.post = post_text
        post.save()

        return JsonResponse({
            "response": "Post Updated"
        })
    else:
        other_user = request.GET.get("user")
        current_user = request.user.username
        id = request.GET.get("id")

        if other_user == current_user:
            post = Posts.objects.get(id=id)

            return render(request, "network/create_post.html", {
                "header": "Edit Post",
                "inputValue": "Save",
                "post": post,
            })
        else:
            return HttpResponseRedirect("/")

def profile(request):
    if request.method == "POST":
        pass
    else:
        other_user = request.GET.get("user")
        current_user = request.user.username

        # Gets the users following and follower count
        user = list(User.objects.filter(username=other_user).values())
        following = user[0]['following']
        followers = user[0]['followers']

        posts = list(Posts.objects.filter(username=other_user).order_by("-id").values())

        following_list = Following.objects.filter(username=current_user).filter(following_username=other_user)

        # Determines how the follow/unfollow button should be displayed
        if other_user == current_user:
            is_following = 0
        elif len(following_list) > 0:
            is_following = 1
        elif len(following_list) == 0:
            is_following = 2

        # Paginate the posts
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        if len(posts) <= 10:
            paginate = False
        else:
            paginate = True

        liked_list = []

        liked = list(Liked.objects.filter(username=current_user).values())

        for i in liked:
            liked_list.append(i["post_id"])

        return render(request, "network/profile.html", {
            "posts": page_obj,
            "username": other_user,
            "following": following,
            "followers": followers,
            "is_following": is_following,
            "paginate": paginate,
            "current_user": current_user,
            "liked": liked_list,
        })

def following(request):
    if request.method == "POST":
        btn_text = request.POST["btnText"].strip()
        following_username = request.POST["username"].strip()
        current_user = request.user.username

        current_user_profile = User.objects.get(username=current_user)
        other_user_profile = User.objects.get(username=following_username)

        if btn_text == "Unfollow":
            # Removes a user from the current user following list
            Following.objects.filter(username=current_user).filter(following_username=following_username).delete()

            # Subtract from the current user following count
            current_user_profile.following = current_user_profile.following - 1
            current_user_profile.save()

            # Subtract from the user the current user is following followers count
            other_user_profile.followers = other_user_profile.followers - 1
            other_user_profile.save()
        else:
            # Adds a user to the current user following list
            Following(
                username = current_user,
                following_username = following_username
            ).save()

            # Adds to the current user following count
            current_user_profile.following = current_user_profile.following + 1
            current_user_profile.save()

            # Adds to the user the current user is following followers count
            other_user_profile.followers = other_user_profile.followers + 1
            other_user_profile.save()

        return JsonResponse({
            "response": "success",
            "btnText": btn_text,
        })
    else:
        username = request.user.username

        following = list(Following.objects.filter(username=username).values())

        following_list = []

        for i in following:
            following_list.append(i["following_username"])

        # Paginate the posts
        posts = Posts.objects.filter(username__in=following_list).order_by("-id")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        if len(posts) == 0:
            msg = "No Posts to display. Follow more people to view their posts"
        else:
            msg = ""

        if len(posts) <= 10:
            paginate = False
        else:
            paginate = True

        liked_list = []

        liked = list(Liked.objects.filter(username=username).values())

        for i in liked:
            liked_list.append(i["post_id"])

        return render(request, "network/index.html", {
            "header": "Following",
            "posts": page_obj,
            "msg": msg,
            "paginate": paginate,
            "liked": liked_list,
        })

def likes(request):
    if request.method == "POST":
        current_user = request.user.username
        id = request.POST["id"]
        link_txt = request.POST["link-txt"]

        post = Posts.objects.get(id=id)

        if link_txt == "like":
            # Increases the like count
            post.likes = post.likes + 1
            post.save()

            # Adds the user to the like table
            Liked(
                post_id = id,
                username = current_user,
            ).save()
        else:
            # Decreases the like count
            post.likes = post.likes - 1
            post.save()

            # Deletes the user from the like table 
            Liked.objects.filter(post_id=id).filter(username=current_user).delete()

        return JsonResponse({
            "response": "Post liked",
            "linkTxt": link_txt,
            "postID": id,
        })