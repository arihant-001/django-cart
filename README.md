# Django-Cart

`django-cart` is a basic model for ecommerce websites implemented using `django` and `postres`.

## Project Setup on localhost

### Clone the repository
```sh
$ git clone https://github.com/arihant-001/django-cart.git
```

### Install and activate virtual environment
```sh
# install virtualenv for easily setting up virtual environment
$ sudo pip3 install virtualenv

# create a new virtual environment with name venv
$ virtualenv -p python3 venv

# activate the venv environment
$ source venv/bin/activate

# If your shell changes like below, then you are ready
(venv) $ 
```

### Install Requirements
```sh
$ pip3 install -r requirements.txt
```

### Run the project
```sh
# inside the cloned directory
$ python3 manage.py runserver
```

## Docker
Set the database config in `django-cart/settings.py` as:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
```
Install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/)

Build and run the container using `docker-compose`
```sh
# Build and start containers
$ doker-compose up --build

# create tables
$ docker-compose exec web python manage.py migrate

# create admin
$ docker-compose exec web python manage.py createsuperuser
```

Create dummy data
```sh
# open web container shell
$ docker exec -it django-cart_web_1 bash

# go to scripts
$ cd scripts

# download data
$ python bb_scrapper.py

# populate data in db
$ python populate_product.py
```

## Heroku 
### Creating new app using heroku cli
```sh
# create an app on heroku with a unique_app_name
$ heroku create unique_app_name

# create tables in database 
$ heroku run python manage.py migrate

# create an admin
$ heroku run python manage.py createsuperuser
```

### Setup production variables 
create a secret key for production using a [key generator](https://miniwebtool.com/django-secret-key-generator/)

```sh
# set the above key in production
$ heroku config:set DJANGO_SECRET_KEY='!oxq(v+a2h-lk!%434t_$g)7li%%318gn6bw1$j1e%7j#h%ahv'

# disable debug 
$ heroku config:set DJANGO_DEBUG=False
```

### Add host in settings
Open /django-cart/settings.py and change the ALLOWED_HOSTS setting to include your base app url 
```python
ALLOWED_HOSTS = ['<your app URL without the https:// prefix>.herokuapp.com','localhost']                                                                                        
```
deploy the updated app
```sh
git add -A
git commit -m 'Update ALLOWED_HOSTS with site and development server URL'
git push heroku master
```