from django.db import models
from django.utils.text import slugify
from versatileimagefield.fields import VersatileImageField, PPOIField

# Create your models here.

def upload_media(instance, filename):
    return 'images/{0}/{1}'.format(instance.shirt.id, filename)


class Brand(models.Model):
    code = models.SlugField(max_length=200, blank=True, editable=False, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)


class PrintType(models.Model):
    code = models.SlugField(max_length=200, blank=True, editable=False, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = slugify(self.name)
        super(PrintType, self).save(*args, **kwargs)


class Shirt(models.Model):
    code = models.SlugField(max_length=200, blank=True, editable=False, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, null=True, blank=True)
    print_type = models.ManyToManyField(PrintType)
    shirt_brand = models.ManyToManyField(Brand)
    featured = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    price = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_featured(self):
        return self.featured

    def is_best_seller(self):
        return self.best_seller

    def get_available_sizes(self):
        text = ''
        for inventory in self.inventory.all():
            if inventory.stock > 0:
                if text == '':
                    text = inventory.size.name
                else:
                    text = ', '.join([text, inventory.size.name])
        return text

    def get_print_type(self):
        return ', '.join([ print_type.name for print_type in self.print_type.all() ])

    def get_shirt_brand(self):
        return ', '.join([ shirt_brand.name for shirt_brand in self.shirt_brand.all() ])

    def save(self, *args, **kwargs):
        self.code = slugify(self.name)
        super(Shirt, self).save(*args, **kwargs)

    class Meta:
        ordering = ["name"]


class Image(models.Model):
    shirt = models.ForeignKey(Shirt, related_name='image', on_delete=models.CASCADE)
    image = VersatileImageField(
        'Image',
        upload_to=upload_media,
        ppoi_field='center_point')
    center_point = PPOIField('Image Center Point of Interest')
    weight = models.PositiveSmallIntegerField(default=9)

    def __str__(self):
        return '{0} - {1}'.format(self.shirt.name, self.weight)

    class Meta:
        ordering = ["weight", "shirt"]


class Size(models.Model):
    code = models.SlugField(max_length=200, blank=True, editable=False, unique=True)
    name = models.CharField(max_length=200)
    size_guide = models.CharField(max_length=200, null=True, blank=True)
    weight = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = slugify(self.name)
        super(Size, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('code', 'weight')
        ordering = ['weight']


class Inventory(models.Model):
    shirt = models.ForeignKey(Shirt, related_name='inventory', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return '{0} - {1}'.format(self.shirt.name, self.size.name)

    class Meta:
        unique_together = ('shirt', 'size')
        ordering = ['-stock','shirt', 'size']


class Gallery(models.Model):
    shirt = models.ForeignKey(Shirt, related_name='gallery', on_delete=models.CASCADE)
    image = VersatileImageField(
        'Image',
        upload_to=upload_media,
        ppoi_field='center_point')
    center_point = PPOIField('Image Center Point of Interest')
    credit = models.CharField(max_length=200, null=True, blank=True)
    weight = models.PositiveSmallIntegerField(default=9)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} - {1}'.format(self.shirt.name, self.image.name)

    class Meta:
        ordering = ['weight', 'updated_at']
