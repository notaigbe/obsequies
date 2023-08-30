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
            (10, 'Son-In-law'),
            (11, 'Daughter-In-law'),
            (12, 'Friend'),
            (13, 'Admirer'))


class Tribute(models.Model):
    title = models.CharField(max_length=200)
    # slug = models.SlugField(max_length=200)
    email = models.EmailField(unique=True)
    author = models.CharField(max_length=200)
    relation = models.CharField(max_length=50)
    updated_on = models.DateTimeField(auto_now=True)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='visitors')
    status = models.IntegerField(choices=STATUS, default=0)

    def user_directory_path(self):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return "visitor/{0}".format(self.picture)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return '{} - {}'.format(self.title, self.author)


class Profile(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    biography = models.TextField()

    def __str__(self):
        return self.title


READING = (
    ('FR', 'FIRST READING'), ('RP', 'RESPONSORIAL PSALM'), ('SR', 'SECOND READING'), ('GA', 'GOSPEL ACCLAMATION'),
    ('GR', 'GOSPEL'))
MASS = (('VM', 'VIGIL MASS'), ('FM', 'FUNERAL MASS'))
HYMNS = (('EH', 'ENTRANCE'), ('OH', 'OFFERTORY'), ('C', 'CONSECRATION'), ('CH', 'COMMUNION'), ('RH', 'RECESSIONAL'))
POINTS = (('0', 'the Church'),
          ('1', 'the repose of his soul'),
          ('2', 'all the mourners'),
          ('3', 'the afflicted'),
          ('4', 'all present'),
          ('5', 'the children, family members, friends and well-wishers'),
          ('6', 'safe journey'),
          ('7', 'a happy death'))


class Mass(models.Model):
    mass = models.CharField(max_length=200, choices=MASS, default=0, unique=True)

    def __str__(self):
        return self.get_mass_display()

    class Meta:
        verbose_name_plural = 'Mass'


class Reading(models.Model):
    reading = models.CharField(max_length=20, choices=READING, default=0)
    passage = models.CharField(max_length=200)
    theme = models.CharField(max_length=200)
    body = models.TextField()
    mass = models.ForeignKey(Mass, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.mass.get_mass_display(), self.get_reading_display())

    class Meta:
        unique_together = ('reading', 'mass')


class Hymn(models.Model):
    hymn = models.CharField(max_length=20, choices=HYMNS, default=0)
    number = models.IntegerField()
    title = models.CharField(max_length=200)
    body = models.TextField()
    mass = models.ForeignKey(Mass, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.mass.get_mass_display(), self.get_hymn_display())

    class Meta:
        unique_together = ('hymn', 'mass', 'number')


class Prayer(models.Model):
    point = models.CharField(max_length=20, choices=POINTS, default=0)
    number = models.IntegerField()
    name = models.CharField(max_length=200)
    body = models.TextField()
    mass = models.ForeignKey(Mass, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.mass.get_mass_display(), self.get_point_display())

    class Meta:
        unique_together = ('point', 'mass', 'number')


class Family(models.Model):
    relationship = models.CharField(max_length=50, choices=RELATION)
    count = models.IntegerField()

