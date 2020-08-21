from django.db import models
from django.contrib.auth.models import User


class CartUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True, null=True)

    def __str__(self):
        return self.name
