from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from pytils.translit import slugify
from decimal import Decimal
from django.core.validators import MinValueValidator


def slug_create(self):
    slug = slugify(self.name)
    slug_exists = True
    counter = 1
    self.slug = slug
    while slug_exists:
        try:
            slug_exits = self._meta.model.objects.get(slug=slug)
            if slug_exits:
                slug = self.slug + '_' + str(counter)
                counter += 1
        except self._meta.model.DoesNotExist:
            self.slug = slug
            break


class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return '{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            slug_create(self)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return '{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            slug_create(self)
            self.created_at = timezone.now()
            self.modified_at = timezone.now()
        else:
            self.modified_at = timezone.now()
        super(Product, self).save(*args, **kwargs)
