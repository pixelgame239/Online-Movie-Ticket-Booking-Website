#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status.
set -o errexit

# Install Python dependencies from requirements.txt
pip install -r requirements.txt

# Collect static files into the STATIC_ROOT directory
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate