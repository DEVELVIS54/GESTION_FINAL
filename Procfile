web: python manage.py collectstatic --noinput && python manage.py migrate && python manage.py createsuperuser --noinput || true && gunicorn gif.wsgi:application
