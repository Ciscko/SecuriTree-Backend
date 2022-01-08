#!/bin/sh -c
#set -eu
export $PORT
envsubst '${PORT}' < /etc/nginx/http.d/nginx.conf > /etc/nginx/http.d/default.conf
exec "$@"
#gunicorn --bind=0.0.0.0:8080 --worker-class=gthread --workers=2 --threads=4 securii.wsgi & nginx -g "daemon off;"