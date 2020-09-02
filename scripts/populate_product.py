import csv
import os
from django.core import files
from io import BytesIO
import requests
import django
import sys

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django-cart.settings")
django.setup()

from catalog.models import Product, Category


def populate_category(category_name):
    category = Category.objects.create(
        name=category_name,
    )
    category.save()
    return category


def populate_products(category):
    file_name = 'dummy_data/' + category.name + '.csv'
    with open(file_name) as csv_file:
        rows = list(csv.reader(csv_file, delimiter=','))
        for i in range(1, len(rows)):
            row = rows[i]
            product = Product.objects.create(
                category=category,
                name=row[0],
                price=row[1],
                description=row[3],
            )
            image_url = row[2]
            resp = requests.get(image_url)

            fp = BytesIO()
            fp.write(resp.content)
            file_name = image_url.split("/")[-1]
            product.image.save(file_name, files.File(fp))

            product.save()


categories = ['fruits-vegetables', 'beverages']
for c in categories:
    category = populate_category(c)
    populate_products(category)
