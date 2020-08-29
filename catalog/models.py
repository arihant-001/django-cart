from django.db import models
from django.urls import reverse
from datetime import datetime


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField()
    category = models.ForeignKey("catalog.Category", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = '/images/placeholder.png'
        return url

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})
