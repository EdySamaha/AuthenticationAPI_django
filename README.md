# Authentication API for Django-based websites
Django backend containing APIs to authenticate a user through CRUD operations on the 'Account' database. **Also supports password hashing and JWT tokens.**

You can test this system using *Postman*, or the user interface implemented through HTML files in the 'templates' folder to visualize the APIs' responses 

## Installation:
Requires [Python 3](https://www.python.org/downloads/)

Clone directory to your computer and open your terminal in this directory.

Run `pip install -r requirements.txt` to install requirements

#### Setup:
In the project directory run the following in order:

`python manage.py makemigrations`

`python manage.py migrate`

(Not necessary: If you want to delete the data already in the database, you can run "python manage.py flush")

`python manage.py runserver 8000` (to run on localhost port 8000)

## Usage:
Send requests to the following APIs:
- `/api-register` create user
- `/api-login` login user
Must be authenticated (i.e. registered or loggedin):
- `/logout` logout user by deleting saved token
- `/api-update` Update user data with id taken from session token variable
- `/api-delete` Delete user with with id taken from session token variable
FOR DEVS ONLY:
- `/api-getuser/id` returns user with specific id
- `/api-getall` returns all users

Account model attributes:
```
{'user_id', 'username', 'email', 'password'}
```
#### NOTE: if you are receiving this data, you must decode JWToken before being able to read these attributes. You should use the `decodeJWT` function defined in views.py

