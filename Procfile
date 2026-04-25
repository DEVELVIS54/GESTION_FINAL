web: python manage.py collectstatic --noinput && python manage.py migrate && python manage.py createsuperuser --noinput || echo "superuser exists" && gunicorn gif.wsgi:application
