# IIS project - Electronic health card information system

## Install dependencies + setup

- Windows:
  - Git, Python 3 + pip3, [PostrgreSQL](https://www.postgresql.org/download/), [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
- Linux (Debian/Ubuntu/PopOS):
  - ```sudo apt install -y git python3 python3-pip postresql libpq-dev snap```
  - ```sudo snap install --classic heroku```
  
- ```heroku login```
- Clone the repository, ```cd vut-fit-iis```
- Run the setup:
  - Windows:
  ```heroku local setup -f Procfile.windows``` or ```pip install --user -r requirements.txt```
  - UNIX-like:
  ```heroku local setup``` or ```pip3 install -r requirements.txt```

## Start the project locally

- First step when not already ran: ```heroku local collectstatic```
- Run the server:
  - Windows:
  ```heroku local web -f Procfile.windows``` or ```python manage.py runserver 0:5000```
  - UNIX-like:
  ```heroku local web``` or ```python3 manage.py runserver 0:5000```
- Open browser at: ```localhost:5000```

## Pushing changes to the repository

Use **VS Code** Git GUI (RECOMMENDED), etc. or manually:

- ```git add .```
- ```git commit -m "Message"```
- ```git push```

## Web deployment

Site is automatically deployed when pushed to Github repository if everything is OK.

Test the site beforehand!

## Files

In ```/hospital``` folder is the project folder for the whole website.

In ```/landing_page``` and ```/user_profile``` folders are 'apps', each app contains different part of ```hospital``` project - ```landing_page``` and ```user_profile``` will display different things, have different logic, etc.

## Databases

Both local project and deployed web is running on the same online database. Every migration, even local, will make changes to the DB.

When made changes to ```model.py``` files, you have to run:

- ```heroku local migrate```

which will update (create/delete/...) corresponding DB tables.

### Using local DB for testing, etc.

If you want to use a local DB, or you want to do some ***crazy sh!t*** which could damage the current DB, please create file ```.local``` in the root directory and run ```heroku local migrate``` to pollute the local DB (to create the same DB structures...).

However keep in mind the new local DB will be empty when used for the first time (DB is just created) and is just **local**, i.e. it won't be pushed to Github and used by the deployed project.

When the code is cleaned up and you are ready to use the online DB, just delete the ```.local``` file and Django will stop using the local DB. The local DB will remain in your folder unless you delete it too (```db.sqlite3```).

### Using the /admin to edit DB entries

You can add/delete/edit entries in the DB manually (***just don't***...), or you can use the ```site-url.com/admin``` page when owning a superuser account.
