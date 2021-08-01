from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Credit(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    Credit_Points = models.IntegerField()


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def get_comments(self):
        return self.comments.all().order_by('-created_date')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})


class StartupSubmissionList(models.Model):
    name = models.CharField(max_length=100)
    site = models.CharField(max_length=256, null=True, blank=True)
    site_type = models.CharField(max_length=256, null=True, blank=True)
    da_score = models.IntegerField(default=0)
    monthly_traffic = models.IntegerField(default=0)
    follow_unfollow_link = models.CharField(max_length=256, null=True, blank=True)
    user = models.ManyToManyField(User, blank=True, related_name='user_list')

    def __str__(self):
        return f'{self.name} - {self.id}'

    class Meta:
        verbose_name_plural = "Startup Submission List"
        ordering = ['id']


# class SSListUser(models.Model):
#     name = models.ForeignKey(SSList, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#
#     def __str__(self):
#         return f'{self.name} - {self.user}'
