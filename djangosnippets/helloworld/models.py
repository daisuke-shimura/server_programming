from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Helloworld(models.Model):
    title = models.CharField('タイトル', max_length=128)


    code = models.TextField('コード', blank=True)
    description = models.TextField('説明', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name='投稿者',
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField('投稿日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    def __str__(self):
        return self.title


class User(AbstractUser):
    university = models.CharField(max_length=128, null=True, blank=True)
    school_year = models.PositiveIntegerField(null=True, blank=True)
    is_manager = models.BooleanField(default=False)


class Lecture(models.Model):
    name = models.CharField(max_length=128)
    body = models.TextField(null=True, blank=True)
    university = models.CharField(max_length=128, null=True, blank=True)
    school_year = models.IntegerField(null=True, blank=True)
    average_score = models.FloatField(null=True, blank=True)
    reviews_count = models.IntegerField(default=0, blank=True)


class Review(models.Model):
    title = models.CharField(max_length=128)
    comment = models.TextField(null=True, blank=True)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
