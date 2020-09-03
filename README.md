# Django-Cart

`django-cart` is a basic model for ecommerce websites implemented using `django` and `mongodb`.

## Project Setup on localhost

### Clone the repository
```zsh
$ git clone https://github.com/arihant-001/django-cart.git
```

### Install and activate virtual environment
```zsh
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
```zsh
$ pip3 install -r requirements.txt
```

### Run the project
```zsh
# inside the cloned directory
$ python3 manage.py runserver
```

## Docker
Install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/)
```zsh
# Build and start containers
$ doker-compose up --build

# create tables
$ docker-compose exec web python manage.py migrate

# create admin
$ docker-compose exec web python manage.py createsuperuser
```

Create dummy data
```zsh
# open web container shell
$ docker exec -it django-cart_web_1 bash

# go to scripts
$ cd scripts

# download data
$ python bb_scrapper.py

# populate data in db
$ python populate_product.py
```