# store_manager_api
[![Build Status](https://travis-ci.org/charitymarani/store_manager_api.svg?branch=Develop)](https://travis-ci.org/charitymarani/store_manager_api)
[![Coverage Status](https://coveralls.io/repos/github/charitymarani/store_manager_api/badge.svg)](https://coveralls.io/github/charitymarani/store_manager_api)
[![Maintainability](https://api.codeclimate.com/v1/badges/54b962ae24d555e4fbfd/maintainability)](https://codeclimate.com/github/charitymarani/store_manager_api/maintainability)

Store Manager api is a simple flask api that powers  a web application that helps store owners manage sales and product inventory records.
### Available Endpoints:
| Http Method | Endpoint Route | Endpoint Functionality |
| :---         |     :---       |          :--- |
| POST   | /api/v1/auth/register     | Creates a user account    |
| POST     | /api/v1/auth/login        | Login a user      |
| POST     | /api/v1/auth/logout       | Logout a user      |
| GET     | /api/v1/auth/users        | Gets all users     |
| GET     | /api/v1/auth/users/username       |Gets a single user by username       |
| POST     | /api/v1/products        | Add a product      |
| POST     | /api/v1/sales        | Add a sales record      |
| GET     | /api/v1/products       | Retrieve all products     |
| GET     | /api/v1/sales       | Retrieve all sales records    |
| GET     | /api/v1/products/productId       | Retrieve a single product by id     |
| GET     | /api/v1/sales/saleId       | Retrieve a single sales record by id     |


### Prerequisites
```
  * pip
  * virtualenv
  * python 3 or python 2.7
```
### Installation
clone the repo

``` 
git clone https://github.com/charitymarani/store_manager_api.git

```

create a virtual environment

```
virtualenv <environment name>

```

activate the environment:

```
$source <Your env name>/bin/activate

```
install dependencies:

```
$pip install -r requirements.txt

```

Run the app, and your ready to go!

```
python run.py

```
### Running the tests
The tests have beene written using the python module unittests. The path to tests folder is `application/tests/v1` for version 1 tests only. Use a test framework like nose to run the tests.
To run the tests use the command:

```
nosetests application/tests/v1

```
### Deployment
The api is deployed on heroku on [THIS](https://store-manager-api123.herokuapp.com/) link

### Documentation
Find the documentation [HERE](https://documenter.getpostman.com/view/5036866/RWguwcJb)

### Built with

Flask, a python framework

### Authors
[Charity Marani](https://github.com/charitymarani)
