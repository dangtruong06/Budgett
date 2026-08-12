#!/bin/sh
set -e
flask db upgrade
exec gunicorn -b 0.0.0.0:5001 "main:create_app()"