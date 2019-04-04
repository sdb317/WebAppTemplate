## Introduction

The aim of this project is to create a web application that leverages Postgres, Django, React and Heroku in order to minimise time-to-market. Repetitive, error-prone manual task are eliminated, where possible, by adopting a model-centric code-generation approach.

The architecture is as follows:

`React/MobX -- RESTapi -- Django -- Postgres`

## Setup

### Path

On Windows, the `bin` folders for the following tools should be added to the `path` environment variable:

* Postgres
* Node
* Heroku

See `env.bat`.

### Python
[Documentation](https://docs.python.org/3/tutorial/venv.html)

Open a command window in the project folder and, using Python 3.6 or later, create a `virtualenv`.

E.g. `"C:\Program Files\Python\3.6\Scripts\virtualenv.exe" env`

Activate it with `env\Scripts\activate` and then test with `python --version`.

Install all dependencies with `pip install -r requirements.txt`.

### Django
[Documentation](https://docs.djangoproject.com/en/2.1/howto/)

Test with `django-admin --version`.

The project is included but can be created with `django-admin startproject _admin app/python`.

The demo app is included but can be created with `django-admin startapp demo app/python/demo`.

### Postgres

Assuming you have installed Postgres locally with the admin username/password as `postgres/postgres`, then start the Postgres CLI with `psql -U postgres` (substitute your username/password as appropriate).

Then from the `sql` prompt, issue the command `create database web_app_template;` followed by `\quit`.

The DATABASE_URL environment variable needs to be set. See `env.bat`.

Test the database setup with `python app\python\manage.py dbshell`.

## Create Models

The `models.py` file is quite different to what you would normally see in a Django project. There is no logic in it as the model 'heavy lifting' is always done in Postgres functions for optimal performance.

Also there are no foreign keys! In this project referential integrity constraints are eschewed as we're all grown-ups and (hopefully) know what we're doing.

There are two special tables:

* definition
* link

They are alphabetically first as they start with a dunderscore.

The first contains global symbolic definitions for the project. A design pattern (described below) is used to ensure the symbolic definitions are always in sync in SQL, Python and Javascript.

The second contains all the links between entities. Anything can be joined to anything via this table. This is almost a 'graph' approach and is designed to provide the ultimate flexibility for creating associations.

The models file also demonstrates the built-in audit pattern that ensure every change to an application table is auditied and can be viewed or re-instated.

Having created the models file, the changes are applied in the usual way with `makemigrations` and `migrate`.

### Add Definitions

For convenience, all definitions are stored in an Excel sheet `admin\AddDefinitions.xlsm`. This allows creation of sequential id's using the 'FillSeries' command. The definitions are stored in a dynamic range `Definitions`.

The first entries in the table should define all the entities in the system using the pattern supplied. This ensures the correct operation of the link table.

To export the definitions, type `<F8>` and run the procedure `UpdateDefinitions`. This creates a new JSON file in the application `fixtures` folder which can then be loaded.

To load these definitions use `python app\python\manage.py updatedefinitions`. This first creates a backup table before loading the new definitions.

Finally, to export the definitions for use in Python and Javascript, run `admin\GetDefinitions.bat <database>`. This creates `definitions.js` and `definitions.py` in the app\js and app\python folders respectively.

### Create Postgres functions

Once the models have been updated in the database, the Postgres functions are automatically generated to reflect the new schema. This approach reduces th number of obscure bugs caused by manually trying to effect the changes.

To create the functions for a table, run `admin\QuerySchema.bat <app> <table>`.

## Project Standards for RESTapi's

This document describes the standards to be applied for **all** RESTapi development. It aims to provide a consistent and intuitive interface between client & server applications.

For Django applications the Django REST Framework package is used to provide a base-level of functionality. Custom classes are then added to override this for specific features e.g to call Postgres user-defined functions instead of Django models.

### API Versioning

The URL should start with a version number e.g. ```/1/employees/```, so that 'breaking changes' can be released while still supporting older clients.

### URL Naming

The URL should only contain resources (nouns), not actions or verbs e.g. ```/employees/``` not ```/addNewEmployee/```

The resource should always be plural in the API endpoint and if we want to access one instance of the resource, we can always pass the id in the URL

By default a standard URL will return HTML. If different content is returned this **must** be specified by using a dot-suffix notation e.g.  ```/employees.xml/``` or ```/employees.json/``` - UNDER REVIEW

All URL's shound end in a forward-slash. ```/```

### HTTP methods

The verbs should be represented by the 4 different HTTP methods: GET, POST, DELETE, PUT

* method ```GET``` path ```/employees/``` should get the list of all employees, or a filtered list if query parameters are supplied
* method ```GET``` path ```/employees/34/``` should get the details of employee 34
* method ```DELETE``` path ```/employees/34/``` should delete employee 34
* method ```POST``` path ```/employees/``` should create a new employee, using the payload supplied, and return a unique identifier for the created record
* method ```POST or PUT``` path ```/employees/34/``` should update the existing employee 34, using the payload supplied

### HTTP response status codes

The server should always return the correct status code to signal the success or failure of the operation to the client

A simplified list of the full HTTP status codes will be used:

#### 2xx (Success category)

* ```200 Ok``` the standard HTTP response representing success for GET, POST, PUT or DELETE

#### 4xx (Client Error Category)

* ```400 Bad Request``` indicates that the request by the client was not processed

In this instance a meaningful "human-understandable" error message should also be returned to the client e.g. 'employee name may not be blank'

#### 5xx (Server Error Category)

* ```500 Internal Server Error``` indicates that the server has thrown an exception during processing

A 'contact support' style of message should be displayed by the client

### HTTP parameters

These can be appended to the URL using the standard ```?name=value&...``` syntax

### HTTP payloads

The payload will typically be either HTML, text, well-formed JSON or XML

The HTTP ```content-type``` header will always be set appropriately


