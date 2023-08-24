from django.db import models
from django.utils import timezone

# Create your models here.
STATUS = ((0, 'DRAFT'), (1, 'PUBLISH'))
RELATION = ((0, 'Wife'),
            (1, 'Son'),
            (2, 'Daughter'),
            (3, 'Brother'),
            (4, 'Sister'),
            (5, 'Cousin'),
            (6, 'Nephew'),
            (7, 'Niece'),
            (8, 'Grandson'),
            (9, 'Granddaughter'),
            (10, 'Son In-law'),
            (11, 'Daughter In-law'),
            (12, 'Friend'),
            (13, 'Admirer'))


class Tribute(models.Model):
    title = models.CharField(max_length=200)
    # slug = models.SlugField(max_length=200)
    email = models.EmailField(unique=True)
    author = models.CharField(max_length=200)
    relation = models.CharField(max_length=200)
    updated_on = models.DateTimeField(auto_now=True)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='visitors')
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title


class Profile(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    biography = models.TextField()

    def __str__(self):
        return self.title