SecuriTree-Backend

This is the Backend API for the securiTree application. This api exposes a list of endpoints which are used by the frontend application to fetch hierarchy data, upload the data from json, manage doors and authenticate the users for every request to the application.

The high-level architectural overview of the whole application is as shown:

![ARCHITECTURE](https://user-images.githubusercontent.com/32708966/149041400-982c55e2-39f2-4878-8d47-3713a4d54bbd.png)

 
The api runs inside a docker container which has got a nginx reverse proxy set up to serve the static files and redirect some requests to the gunicorn webserver gateway interface.

WSGI is bound to Django/python code, since nginx webserver cannot understand python files; WSGI works as the interface between python and nginx. Python code interacts with the SQLITE database using an ORM. The logic for building the hierarchy data object is implemented on the python code. This hierarchy object is stored on a JSON field so that upon request it's simply rendered to the frontend, saving the overhead of the recursive re-structuring.

HOW TO INSTALL ON YOUR PC

METHOD ONE:

1.	Ensure you have docker installed on your PC, since the application is containerized.

2.	Open the CMD and run the following:

4.	o	docker run --name sec-front -p 3000:80 -d francoudev/securitree-repo:securitree-frontend
5.  o	docker run --name sec-back -e SUPERUSER_USERNAME=yourusername -e SUPERUSER_PASSWORD=yourpassword -p 8000:8000 -d francoudev/securitree-repo:securitree-backend
  
6.	This pulls the application images from docker hub and runs the applications. The superuser credentials to login to the application are the values you specify above. Open the browser and navigate to http://localhost:3000. Alternatively to set your own default superuser credentials, you can clone this repo, set your own credentials in the .env environment variables and rebuild the image then run. How to do this? See method 2 below.


METHOD TWO:
1.	As mentioned earlier, the Backend application is containerized, therefore you need to install Docker on your PC before we proceed.
2.	Clone this git repo on your PC.
4.	Create an .env file and fill it with the credentials as shown in the template named as .env-example, the .env file must be in the same folder as Dockerfile or .env-example.
6.	Open CMD inside the same folder as Dockerfile of our project.
8.	Run the following commands:
    o	docker build -t securi-image .
    o	docker run --name securi-back -p 8000:8000 -d securi-image
8.	By this run, we are assuming that on your pc, port 8000 is free and can be used. Otherwise you can use any other port above 1000 if 8000 is used by another application.
10.	Now your API backend is running at http://localhost:8000/api/ - this url is required by your frontend. The .env file of your frontend should have this as the API_URL.
12.	If your frontend was already set up, you should be able to login to your application using the superuser credentials stored in the .env file.
14.	You can login to the backend admin site at http://localhost:8000/admin/ to do manage your models and permissions as a superuser.
16.	You can also login to your frontend application as an ordinary user, using the frontend url endpoint.
18.	After login to the frontend, you can upload the json files on the Upload Data page.
19.	Cheers! That's it.


PROJECT DETAILS

All the technologies used in this application are open source.
This backend API is built with django python web framework. As obtained from their website: "DjangoThe web framework for perfectionists with deadlines."
The framework contains authentication middleware, database object relational mapper, testing suite and an admin panel. These have been leveraged and used to obtain the fully functional backend API.

Containerization using docker ensures the project is portable and can be deployed easily in any DEVOPS pipeline or any cloud computing platform with minimal to zero configurations.

Decoupling of the Backend from the Frontend app ensures that the data storage and application logic is agnostic of the presentational layer. It also allows utilization of the stateless authentication mechanisms where user sessions are not required to be stored on the server but the users hold their authentication tokens to the same server regardless of the type of clients used. Therefore the frontend can be a mobile app, a progressive web app, a desktop app, another backend system, a requests' tool like postman or even data analysis tools like Microsoft Power BI and the like. This allows maintainability, scalability and robustness of the application.

AUTHENTICATION

Authentication is achieved using JWT- JSON Web Tokens which is a stateless authentication method. It begins with frontend client sending username and password to the API. The API is configured to respond with Bearer access and refresh tokens. ThE API endpoints are decorated with an authentication decorator functions, therefore they only respond with data if every request contains an authorization header of a Bearer token.

The tokens are built by the SimpleJWT library which takes in the secret key provided in the environment variables to create the signed section of the token. This secret key is kept secret for security purposes. To authenticate a user, user credentials must be stored in the database. Once a user is added, the username, email, names are stored in the database as strings; While the password is hashed with one-way hashing algorithm (PBKDF2 algorithm with a SHA256 hash). This algorithm is provided by django.

There is also an admin panel which utilizes cookie stateful authentication, where by a user sends username and password to the backend; if the backend successfully authenticates that user, it creates a session cookie and sends it back to the browser. The browser utilizes this cookie in every request to the backend. The session data is stored in the backend server. Therefore the admin panel will work with browser clients only while our application which has the frontend utilizing stateless tokens, can be a mobile application, a desktop application that can simply append the header bearer tokens for authentication. Django comes with very powerful goodies that can be customized to suit the needs of a given project.

FUNCTIONS AND THE OBJECT RELATIONAL MAPPER

Inside the apiservice app of the project, there are views and urls. These are mapped to each other and to the endpoints of the API. When a request reaches django, we have defined routing urls which directs those requests to some python functions(views). These views are decorated with authentication decorators to ensure that the request headers contain valid access tokens signed with JWT. If successfully authenticated, views utilize the database ORM to communicate with SQLITE database to CRUD data. This goes for all of the urls provided in the urls file and therefore each url points to a single python function. The API endpoints available are as follows:

GET - https://the_api_url.com/api/ - this returns the json hierarchy object which is used to present the hierarchy on the frontend. It fetches the datafrom a JSON field in the Hierarchy table/relation.

GET - https://the_api_url.com/api/doors/ - this returns the list of available doors. Through the ORM it fetches all the doors available in the database and returns it as a serialized JSON object.

GET - https://the_api_url.com/api/user/ - this returns the details of the user that sent the request. This endpoint simply gets the user data from the request context in a given request.

POST - https://the_api_url.com/api/upload/ - this expects a post request with a payload of system_data.json of field named as "datafile". This view calls a function that reads system data from the json file. On the returned data, then separately fetches all the areas, doors and accessrules and adds them to their respective tables obeying their relational constraints.

In addition, the upload view calls a function that builds the hierarchichal model of the data ensuring that doors are nested inside their parent areas and accessrules are nested inside the areas based on the available doors for that area. This list of areas containing doors and accessrules is then passed to a recursive formula.

The recursion formula which is called contains a base case of an area object without children areas and non-base cases that contain children areas based on the parent _area_id self-referencial field. Tjis function nests all the areas inside their parents and the result is a single JSON object with the parent area as the top-most object containing all the other nested areas.

Finally the JSON object is stored in a JSON field of the Hierarchy table. This ensures that each time a user visits the View Hierarchy page, the hierarchy is automatically fetched and not constructed saving the time taken by recursive function. Recursive functions can be very expensive. Each time a new system data file is added, the Hierarchy object is constructed and replaced in the table.

POST - https://the_api_url.com/api/upload_users/ - this endpoint expects a post request with a payload of users_data.json of field named as "datafile". This view calls a function that reads users data from the json file. The returned data is then by iteration passed through the ORM's create_user method which automatically hashes the passwords and stores the other user details in string fields. This users will be able to login to the SecuriTree application.

POST - https://the_api_url.com/api/lock_door/ - this expects a post request with payload of two fields "door_id" and "state", state can be open/closed. This view fetches for the door using its ID by the ORM and updates the status as the sent value. Then the Hierarchy JSON object is reconstructed and updated in the database.

POST - https://the_api_url.com/api/token/ - this expects a post request with payload of two fields "username" and "password", it returns the token used for authentication as a Bearer token in subsequent requests. This function is called during login. The returned tokens are stored by the client and used in the other requests until the token expires and the user is required to login again.


THE ADMIN PANEL

Django gives an out of the box admin panel which lists all the relational tables data. Therefore, the accessrules, doors and areas are listed with all the CRUD actions available. This panel also allows the permissions of a certain user to be managed by the superuser. A user can also be deleted, disabled, updated or added. This ensures the superusers have full control on the application data. Emptying the database tables would also happen in this panel if need be, although it can also be done by uploading empty JSON arrays. The superuser is automatically created during the build of the application using the provided environment variables. The admin panel can be accesed at: http://localhost:8000/admin/



TESTS SUITE

Inside the apiservice app of the project, there is a tests.py file which contain the different unit tests for our API. Django provides an assertion library which allows us to do assertions on every view and function, the models and also our urls using the python Client module to mimic actual user requests.


LOGGING

To view the logs generated by the application, run the following commands on the CMD:
1.	o	docker logs sec-back > backend_logs.txt
2.	o	docker logs sec-front > frontend_logs.txt

3.	This will put the logs generated by the application into the files as shown.
4.	The backend application has the logging mechanism configured. Docker automaically detects the logs and are handled by the container, therefore we are able to obtain them by the above commands.


PROCESS ALGORITHMS


![UPLOADING OF USERS](https://user-images.githubusercontent.com/32708966/149040042-f2461bfc-0eb2-47ae-8100-9fd5a8fe4f75.png)


![Upload Process](https://user-images.githubusercontent.com/32708966/149040068-531fea6a-01a3-4b21-bae9-aab25d0396a3.png)


![Recusive render](https://user-images.githubusercontent.com/32708966/149040089-01c8cacd-48de-469e-aca7-7d9751616f11.png)



 
 
 
