# Authentication API for Django-based websites
Django backend containing APIs to authenticate a user through CRUD operations on the 'Account' database. **Also supports password hashing and JWT tokens.**

I recommend using *Postman* to test this system. The HTML files in the 'templates' folder can be used to visualize the APIs' responses by uncommenting the "VISUALS" sections in the views.py code.

#### Installation:
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
- `/register` create user
- `/login` login user
- `/logout/id` logout user with specific id
- `/getuser/id` returns user with specific id
- `/getall` returns all users
- `/update/id` Update user data
- `/delete/id` Delete user with specific id (Note: this needs to be more secure)

Account model attributes:
```
{'user_id', 'username', 'email', 'password'}
```
#### NOTE: if you are receiving this data, you must decode JWToken before being able to read these attributes. You should use the `decodeJWT` function defined in views.py

