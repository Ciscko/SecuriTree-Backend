# SecuriTree-Backend
This is the Backend API for the securiTree application. This api exposes a list of endpoints which are used by the frontend application to fetch hierarchy data, upload the data from json, manage doors and authenticate the users for every request to the application.

The high-level architectural overview of the whole application is as shown:

![ARCHITECTURE](https://user-images.githubusercontent.com/32708966/148338777-df732cda-7454-4f42-a163-6137d80e388a.png)

The api runs inside a docker container which has got a nginx reverse proxy set up tp serve the static files and redirect some requests to the gunicorn webserver gateway interface.

WSGI runs Django/python code. Python code interacts with the SQLITE database. The logic for building the hierarchy data object is implemented on the python code. This hierarchy object is stored on a JSON field so that upon request it's simply rendered to the frontend, saving the overhead of the recursive re-structuring.

The API endpoints available are as follows:

GET - https://the_api_url.com/api/ -  this returns the json hierarchy object which is used to present the hierarchy on the frontend

GET - https://the_api_url.com/api/doors/ - this returns the list of available doors

GET - https://the_api_url.com/api/user/ - this returns the details of the logged in user sending the requests

POST - https://the_api_url.com/api/upload/ - this expects a post request with a payload of system_data.json of field named as "datafile"

POST - https://the_api_url.com/api/upload_users/ - this expects a post request with a payload of users_data.json of field named as "datafile"

POST - https://the_api_url.com/api/lock_door/ - this expects a post request with payload of two fields "door_id" and "state", state can be open/closed

POST - https://the_api_url.com/api/token/ - this expects a post request with payload of two fields "username" and "password", it returns the token used for authentication as a            Bearer token in subsequent requests

HOW TO INSTALL ON YOUR PC
1. As mentioned earlier, the Backend application is containerized, therefore you need to install Docker on your PC before we proceed.
2. Clone this git repo on your PC.
3. Create an .env file and fill it with the credentials as shown in the template named as .env-example
4. Open CMD inside the same folder as Dockerfile of our project.
5. Run the following commands:
6.  - docker build -t securi-image .
7.  - docker run --name securi-back -p 8000:8000 -d securi-image
8.  By this run, we are assuming that on your pc, port 8000 is free and can be used. Otherwise you can use any other port above 1000 if 8000 is used by another application.
9.  Now your API backend is running at http://localhost:8000/api/ - this url is required by your frontend. The .env file of your frontend should have this as the API_URL.
10.  If your frontend was already set up, you should be able to login to your application using the superuser credentials stored in the .env file.
11.  You can login to the backend admin site at http://localhost:8000/admin/ to do manage your models and permissions as a superuser.
12.  You can also login to your frontend application as an ordinary user, using the frontend url endpoint.
13.  After login to the frontend, you can upload the json files on the Upload Data page.
14.  Cheers! That's it.

