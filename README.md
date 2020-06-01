## Web application

#### Technical task of the application:
- the site at the opening shows the "log in" button;
- by pressing does oauth authorization VKontakte;
- shows the name of the authorized user;
- shows 5 any friends of the user;
- at subsequent launches / visits to the page, it immediately displays all the information as it already understands that it is authorized and authorization is remembered.

#### Application Launch:
1. Register a site in `VKontakte` to gain access to the API;
1. Clone the repository: 
    ```git clone https://github.com/leeuw12/task_auth_project.git```
1. Modify `config.py` using the data obtained after the first paragraph;
1. Change `default.conf`, replacing "YOUR_DOMAIN" with the domain of your server.
1. Install `docker` and `docker-compose`
1. Launch the docker container using the command: 
    ```
    docker-compose up -d
    ```
1. You can stop the application with the 
    ```
    docker-compose down command
    ```