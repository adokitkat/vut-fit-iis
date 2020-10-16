web: gunicorn hospital.wsgi --log-file -
collectstatic: python3 manage.py collectstatic
setup: pip3 install --user -r requirements.txt
migrate: python3 manage.py migrate
makemigrations: python3 manage.py makemigrations