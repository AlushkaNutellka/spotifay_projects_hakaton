from django.contrib.auth import get_user_model
from django.db import models
from slugify import slugify

User = get_user_model()


class MusicInfo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=30)
    body = models.TextField()
    music = models.FileField(upload_to='music_inst/', blank=True)
    image = models.ImageField(upload_to='posts/', blank=True)
    slug = models.SlugField(max_length=30, primary_key=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def avg_rating(self):
        from django.db.models import Avg
        result = self.rating.aggregate(Avg('rating'))
        return result['rating__avg']

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    comment = models.CharField(max_length=30)
    post = models.ForeignKey(MusicInfo, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.comment


class Rating(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField()
    post = models.ForeignKey(
        MusicInfo, on_delete=models.CASCADE, related_name='ratings'
    )

    def __str__(self) -> str:
        return f'{self.rating} -> {self.post}'


class Like(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes'
    )
    post = models.ForeignKey(
        MusicInfo, on_delete=models.CASCADE, related_name='likes'
    )
    is_liked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.post} Liked by {self.author.name}'
