FROM python:3.10.0-alpine
ENV PYTHONUNBUFFERED=1

#install bash to enable do bash commands
RUN apk add --no-cache bash

#install nginx 
RUN apk add --no-cache nginx
RUN apk add gettext
#set nginx folders for logs
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

#copy and install python project dependencies
COPY requirements_docker.txt .
RUN pip install --no-cache-dir -r requirements_docker.txt

#configure the reverse proxy port, sername and folder for static files
COPY nginx.conf /etc/nginx/http.d/nginx.conf

#Set the working directory of our app and copy our project into it
WORKDIR /usr/src/app
COPY . /usr/src/app

#ENV PORT=8080
#ARG PORT=8080\
#RUN chmod +x docker-entrypoint.sh
#ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
#Run nginx and the WSGI with gunicorn and bind it to the port assigned from nginx proxy pass
CMD gunicorn --bind=0.0.0.0:8080 --worker-class=gthread --workers=2 --threads=4 securii.wsgi & nginx -g "daemon off;"