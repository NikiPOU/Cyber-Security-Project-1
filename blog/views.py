from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .models import Post
from django.db import connection

def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})

def add_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        Post.objects.create(title=title, content=content)
        return redirect("home")
    return render(request, "add_post.html")

# FLAW 1, Example 1: deleting a post, VULNERABLE
# FIX: allow delete only via POST requests, not GET (fix commented out)

def delete_post(request, post_id):

    #if request.method != "POST":
    #   return HttpResponseForbidden("Delete not allowed via GET")

    post = Post.objects.get(id=post_id)
    #if post.owner != "admin":
    #    return HttpResponseForbidden("You can't delete this post.")

    post.delete()
    return redirect("home")


# Search for post title (vulnerable)
def search(request):
    query = request.GET.get("title", "")
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM blog_post WHERE title LIKE '%{query}%'")
        results = cursor.fetchall()
    return render(request, "search.html", {"results": results})

from .models import User

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # bad, Comparing plaintext password directly
        try:
            user = User.objects.get(username=username, password=password)
            return HttpResponse(f"Welcome back, {user.username}!")
        except User.DoesNotExist:
            return HttpResponse("Invalid login")
    return render(request, "login.html")
