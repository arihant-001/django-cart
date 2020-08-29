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