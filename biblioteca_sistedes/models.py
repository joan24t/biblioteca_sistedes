# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Article(models.Model):

    # Attributes
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    author_ids = models.ManyToManyField('Author')
    keyword_ids = models.ManyToManyField('Keyword')
    access_right_ids = models.ManyToManyField('AccessRight')
    track_ids = models.ManyToManyField('Track')
    edition_id = models.ForeignKey('Edition', on_delete=models.CASCADE)
    file = models.FileField(upload_to="media/", null=True, blank=True)
    url_file = models.CharField(max_length=1000)
    description = models.TextField(max_length=1000)
    user_ids = models.ManyToManyField('User')


class AccessRight(models.Model):

    # Attributes
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    article_ids = models.ManyToManyField('Article')


class Author(models.Model):

    # Attributes
    name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    article_ids = models.ManyToManyField('Article')


class Conference(models.Model):

    # Attributes
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)

# class File(models.Model):
#
#     #Attributes
#     name = models.CharField(max_length=100)
#     domain = models.CharField(max_length=100)


class User(models.Model):

    # Attributes
    name = models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    rol = models.IntegerField()
    edition_ids = models.ManyToManyField('Edition')
    track_ids = models.ManyToManyField('Track')
    article_ids = models.ManyToManyField('Article')


class Edition(models.Model):

    # Attributes
    name = models.CharField(max_length=100)
    preamble = models.TextField(max_length=1000)
    description = models.TextField(max_length=10000)
    year = models.IntegerField()
    place = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    user_ids = models.ManyToManyField('User')
    conference_id = models.ForeignKey('Conference', on_delete=models.CASCADE)


class Keyword(models.Model):

    # Attributes
    name = models.CharField(max_length=100)
    article_ids = models.ManyToManyField('Article')


class Track(models.Model):

    # Attributes
    name = models.CharField(max_length=100)
    preamble = models.TextField(max_length=1000)
    description = models.TextField(max_length=10000)
    edition_id = models.ForeignKey('Edition', on_delete=models.CASCADE)
    user_ids = models.ManyToManyField('User')
    article_ids = models.ManyToManyField('Article')


class Sequence(models.Model):

    # Attributes
    number = models.IntegerField()

    @classmethod
    def get_last_number(self):
        sequence = Sequence.objects.order_by('-number')
        number = sequence[0].number if sequence else -1
        return number


class Bulletin(models.Model):

    # Attributes
    name = models.CharField(max_length=100)
    date = models.DateField()
    url_file = models.CharField(max_length=1000)
    handle = models.CharField(max_length=100)
