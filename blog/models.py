from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    #For Flaw 3, now each post has an owner. 
    #allow deletion only if post.owner == "admin"
    
    #owner = models.CharField(max_length=100, default="admin")  # Simulated owner

    def __str__(self):
        return self.title
