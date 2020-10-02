# IIS projekt - Nemocnica

## Install dependencies + setup

- Windows:
  - Git, Python 3 + pip3, [PostrgreSQL](https://www.postgresql.org/download/), [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
- Linux (Debian/Ubuntu/PopOS):
  - ```sudo apt install -y git python3 python3-pip postresql libpq-dev snap```
  - ```sudo snap install --classic heroku```
  
- ```heroku login```
- Clone the repository, ```cd vut-fit-iis```
- ```heroku local setup```

## Start the app locally

- First step when not already ran: ```heroku local collectstatic``` (DON'T KNOW IF NECESSARY)
- Run the server:
  - On Windows: ```heroku local web -f Procfile.windows```
  - On UNIX-like: ```heroku local web```
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

In ```/hospital``` folder is the project folder for the whole website

In ```/landing_page``` and ```/user_profile``` folders are 'apps', each app contains different part of ```hospital``` project - ```landing_page``` and ```user_profile``` will display different things, have different logic, etc.
