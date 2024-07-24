from django.db import models
from django.template.defaultfilters import slugify
from accounts.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="blog/images")
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='author', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post', null=True)
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
