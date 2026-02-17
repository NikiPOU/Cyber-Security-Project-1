from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from .models import Post, User
from django.db import connection
from django.contrib.auth.hashers import make_password, check_password


def home(request):
    posts = Post.objects.all()
    current_user = request.session.get('username')
    return render(request, "home.html", {"posts": posts, "current_user": current_user})


def add_post(request):
        #Require login to create post
    current_user = request.session.get("username")

    if not current_user:
        return HttpResponseForbidden("You must be logged in to create a post.")
    
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        #Check if user is logged in
        Post.objects.create(
            title=title,
            content=content,
            owner=current_user
        )

        return redirect("/")

    return render(request, "add_post.html")


# FLAW 1, Example 1: deleting a post, VULNERABLE
# FIX: Only allow the owner to delete their own posts

def delete_post(request, post_id):

    current_user = request.session.get("username")

    if not current_user:
        return HttpResponseForbidden("You must be logged in to delete posts.")

    post = Post.objects.get(id=post_id)

    # current_user = request.session.get("username")
    # if post.owner != current_user:
    #     return HttpResponseForbidden("You are not allowed to delete this post.")

    post.delete()
    return redirect("/")


def search(request):
    query = request.GET.get("title", "")
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM blog_post WHERE title LIKE '%{query}%'")
        results = cursor.fetchall()
    return render(request, "search.html", {"results": results})

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
        #Flaw 4: passwords stored in plain text and not hashed.
        #FIX: uncomment out below block of text and comment the line after it.

            #hashed_password = make_password(password)
            #User.objects.create(username=username, password=hashed_password)

            User.objects.create(username=username, password=password)
            return redirect("login")  # send to login page after signup
        else:
            return HttpResponse("Username already exists")
    return render(request, "signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
        #Flaw 4: passwords stored in plain text and not hashed.
        #FIX: uncomment out below block of text and comment the line after it.
            #user = User.objects.get(username=username)
            #if not check_password(password, user.password):
            #    return HttpResponse("Invalid login")
            user = User.objects.get(username=username, password=password)  # plaintext for flaw demo

            request.session['username'] = user.username
            return redirect("home")  # redirect to home page
        except User.DoesNotExist:
            return HttpResponse("Invalid login")
    return render(request, "login.html")

def logout_view(request):
    request.session.flush()
    return redirect("home")

