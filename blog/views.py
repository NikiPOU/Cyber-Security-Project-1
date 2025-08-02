from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .models import Post
from django.db import connection  # for SQL injection demo later

# View all posts
def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})

# Add a new post
def add_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        Post.objects.create(title=title, content=content)
        return redirect("home")
    return render(request, "add_post.html")

# deleting a post, VULNERABLE
# correct solution, allow delete only via POST requests, not GET (commented out)

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
