# django-ecommerce
* Simple API created in Django and Django Rest Framework for creating orders and accessing products


## Tech stack
* Python 3.11
* Django 4.2.5
* Django REST Framework
* PostgreSQL
* Docker with Docker Compose


## Functionalities
* User registration with creating user profiles with address and 2 tiers available (customer or seller).
* As a customer you can add products to the cart and update their quantity and create orders.
* As a seller you are able to add and modify products.
* You can browse + filter products and categories without being registered.


## Project setup
### IMPORTANT:
In order to execute commands with 'make' in Windows you need to install Chocolatey Package Manager
https://chocolatey.org/
Moreover you need to have docker installed in order to run the project containers

1. Clone repository:
`$ git clone https://github.com/mmyszak999/django-ecommerce`
2. In the 'config' directory create '.env' file
3. In '.env' set the values of environment variables (you can copy the content from '.env.template' file)
4. To build the project, in the root directory type:
`$ make build`
5. In order to run project type: 
`$ make up`


## Create migrations and migrate them
`$ make migrations`

## Run Tests
`$ make test`

## Create admin
`$ make superuser`

## Run code formatter
`$ make black`
