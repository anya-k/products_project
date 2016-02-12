from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from pytils.translit import slugify


class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40)
    description = models.TextField()

    def __unicode__(self):
        return '{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return '{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
            self.created_at = timezone.now()
            self.modified_at = timezone.now()
        else:
            self.modified_at = timezone.now()
        super(Product, self).save(*args, **kwargs)
