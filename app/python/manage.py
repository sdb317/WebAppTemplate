#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_admin.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

# python app\python\manage.py runserver --noreload localhost:8000 # runsslserver
# python app\python\manage.py runserver --noreload 0.0.0.0:8000 # For access on local network

# python app\python\manage.py shell
# python app\python\manage.py shell_plus --notebook

