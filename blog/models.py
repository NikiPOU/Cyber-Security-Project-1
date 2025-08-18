from django.db import models
#below for Flaw 4.
#from django.contrib.auth.hashers import make_password 


# FLAW 1, Example 2 (IDOR): Now each post has an owner.
# FIX: allow deletion only if post.owner == "admin" (fix commented out).
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    #owner = models.CharField(max_length=100, default="admin")  # Simulated owner

    def __str__(self):
        return self.title



# FLAW 4: passwords stored in plain text and not hashed.
# FIX: comment out below block of text.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

#    def save(self, *args, **kwargs):
#        # If the password is not already hashed, hash it before saving
#        if not self.password.startswith("pbkdf2_sha256$"):
#            self.password = make_password(self.password)
#        super().save(*args, **kwargs)


    def __str__(self):
        return self.username