#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from pathlib import Path
envpypath = Path(__file__).parent.resolve() / Path("POD/env.py")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'POD.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if len(sys.argv) > 1:
        if sys.argv[1] == 'makesecretkey':
            from django.core.management.utils import get_random_secret_key
            with open(envpypath, 'w') as envpy:
                envpy.write(f"ENV_SECRET_KEY = '{get_random_secret_key()}'")
            return

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
