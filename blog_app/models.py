from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from datetime import datetime


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250,verbose_name= "Tytuł")
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(verbose_name= "Treść")
    img = models.ImageField(default='post_pics/default.png', upload_to='post_pics/', verbose_name= "Obrazek")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    likes = models.ManyToManyField(User, related_name='post_likes', null=True)
    popularity = models.IntegerField(default=0)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_app:post_detail',
                        args=[self.publish.year,
                              self.publish.strftime('%m'),
                              self.publish.strftime('%d'),
                              self.slug])

    def num_of_likes(self):
        return self.likes.count()

    def num_of_comments(self):
        num = Comment.objects.filter(post_id=self.id)
        return num.count()

    def num_of_popularity(self):
        self.popularity = self.num_of_likes()+self.num_of_comments()
        return self.popularity

    def likes_as_flat_user_id_list(self):
        return self.likes.values_list('id', flat=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Komentarz dodany przez dla posta {}'.format(self.post)

    def get_date(self):
        time = datetime.now()
        if self.created.day == time.day:
            return str(time.hour - self.created.hour) + " godzin temu"
        else:
            if self.created.month == time.month:
                return str(time.day - self.created.day) + " dni temu"
            else:
                if self.created.year == time.year:
                    return str(time.month - self.created.month) + " miesięcy temu"
        return self.created


