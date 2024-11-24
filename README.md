# FastAPI eCommerce API

## About
This project is an E-Commerce API built using FastAPI, designed to serve both businesses and end-users.
It utilizes PostgreSQL as the primary database and employs SQLAlchemy and asyncpg for asynchronous database operations.
It uses Pydantic for request validation and schema management. Alembic is used for managing database schema migrations, ensuring a smooth upgrade and rollback of database changes.

This project serves as a strong foundation for developers to build upon.

## Setup
1. Install `git`, `podman`, `postgresql`, `poetry` and `virtualenv` on your development environment.  
   Command
   ```shell
   $ sudo dnf install git podman postgresql poetry virtualenv
   ```
2. Ensure that `podman` service is enabled and started.  
   Command
   ```shell
   $ sudo systemctl enable podman.service
   ```
   Sample output
   ```shell
   Created symlink /etc/systemd/system/default.target.wants/podman.service → /usr/lib/systemd/system/podman.service.
   ```
   Command
   ```shell
   $ sudo systemctl start podman.service
   ```
3. Clone the repository to the local storage.  
   Command
   ```shell
   $ git clone https://github.com/sdglitched/FastAPI-eCom.git
   ```
   Sample output
   ```shell
   Cloning into 'FastAPI-eCom'...
   remote: Enumerating objects: 357, done.
   remote: Counting objects: 100% (357/357), done.
   remote: Compressing objects: 100% (209/209), done.
   remote: Total 357 (delta 219), reused 270 (delta 143), pack-reused 0 (from 0)
   Receiving objects: 100% (357/357), 870.89 KiB | 2.24 MiB/s, done.
   Resolving deltas: 100% (219/219), done.
   ```
   Command
   ```shell
   $ cd FastAPI-eCom
   ```
4. Download the official `postgres` image from `docker.io/library/quay.io` OCI images repository and start a container with your preferred settings.  
   Command
   ```shell
   $ podman pull docker.io/library/postgres:latest
   ```
   Sample output
   ```shell
   Trying to pull docker.io/library/postgres:latest...
   Getting image source signatures
   Copying blob febd2e801cbc done   | 
   Copying blob b5b68d2b7dfa done   | 
   Copying blob 2d429b9e73a6 done   | 
   Copying blob 3234e936b543 done   | 
   Copying blob 0e741c16b01d done   | 
   Copying blob 2bc4b686b410 done   | 
   Copying blob abad6e2f102b done   | 
   Copying blob fc0ed0630c16 done   | 
   Copying blob 15ea73ccc174 done   | 
   Copying blob bc241f8dfdda done   | 
   Copying blob e6b9724cd240 done   | 
   Copying blob 87f78d636266 done   | 
   Copying blob 4bd7a2dad750 done   | 
   Copying blob 4c07baf06858 done   | 
   Copying config 80cbdc6c33 done   | 
   Writing manifest to image destination
   80cbdc6c330118a0a7e082e65be9f54d0d633280aec435a18ad0636095239ad5
   ```
   Command
   ```shell
   $ podman run \
       --name <CONTAINER-NAME> \
       --env POSTGRES_USER=<DATABASE-USERNAME> \
       --env POSTGRES_PASSWORD=<DATABASE-PASSWORD> \
       --env POSTGRES_DB=<DATABASE-NAME> \
       --env PGDATA=/var/lib/postgresql/data/pgdata \
       --volume <MOUNT-LOCATION>:/var/lib/postgresql/data:Z \
       --publish 5432:5432 \
       --restart unless-stopped \
       --detach postgres:latest
   ```
   Sample output
   ```shell
   92cebc2fcee1647a35c27ab4bdfaa6023ba58703fc40a65d85379510bb6456e1
   ```
   Command
   ```shell
   $ podman ps -a
   ```
   Sample output
   ```shell
   CONTAINER ID  IMAGE                              COMMAND     CREATED        STATUS        PORTS                   NAMES
   71e1160d5ed5  docker.io/library/postgres:latest  postgres    3 minutes ago  Up 3 minutes  0.0.0.0:5432->5432/tcp, 5432/tcp  eCom_container
   ```
5. Create a virtual environment in the said directory and activate it. As project does not support python 3.13 virtual environment needs to be of `python3.12`.  
   Command
   ```shell
   $ virtualenv -p python3.12 venv
   ```
   Sample output
   ```shell
   created virtual environment CPython3.12.7.final.0-64 in 431ms
    creator CPython3Posix(dest=/home/sdglitched/FastAPI-eCom/venv, clear=False, no_vcs_ignore=False, global=False)
    seeder FromAppData(extra_search_dir=/usr/share/python-wheels,download=False, pip=bundle, via=copy, app_data_dir=/home/sdglitched/.local/share/virtualenv)
        added seed packages: pip==24.2
    activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator
    ```
   Command
   ```shell
   $ source venv/bin/activate
   ```
   Sample output
   ```shell
   (venv) $
   ```
6. Install the project dependencies.  
   Command
   ```shell
   (venv) $ poetry check
   ```
   Sample output
   ```shell
   All set!
   ```
   Command
   ```shell
   (venv) $ poetry install
   ```
   Sample output
   ```shell
   Installing dependencies from lock file
   
   Package operations: 43 installs, 0 updates, 0 removals
   
      - Installing mdurl (0.1.2)
      - Installing idna (3.7)
      - Installing markdown-it-py (3.0.0)
      - Installing pygments (2.18.0)
      - Installing sniffio (1.3.1)
      - Installing anyio (4.4.0)
      - Installing click (8.1.7)
      - Installing h11 (0.14.0)
      - Installing certifi (2024.7.4)
      - Installing rich (13.7.1)
      - Installing shellingham (1.5.4)
      - Installing typing-extensions (4.12.2)
      - Installing annotated-types (0.7.0)
      - Installing greenlet (3.0.3)
      - Installing markupsafe (2.1.5)
      - Installing httpcore (1.0.5)
      - Installing pydantic-core (2.20.1)
      - Installing python-dotenv (1.0.1)
      - Installing dnspython (2.6.1)
      - Installing httptools (0.6.1)
      - Installing pyyaml (6.0.1)
      - Installing typer (0.12.3)
      - Installing uvloop (0.19.0)
      - Installing watchfiles (0.22.0)
      - Installing websockets (12.0)
      - Installing email-validator (2.2.0)
      - Installing fastapi-cli (0.0.4)
      - Installing jinja2 (3.1.4)
      - Installing pydantic (2.8.2)
      - Installing python-multipart (0.0.9)
      - Installing sqlalchemy (2.0.31)
      - Installing starlette (0.37.2)
      - Installing httpx (0.27.0)
      - Installing orjson (3.10.6)
      - Installing mako (1.3.5)
      - Installing ujson (5.10.0)
      - Installing uvicorn (0.30.1)
      - Installing alembic (1.13.2)
      - Installing bcrypt (4.2.0)
      - Installing psycopg2-binary (2.9.9)
      - Installing asyncpg (0.29.0)
      - Installing ruff (0.7.3)
      - Installing fastapi (0.111.0)
   
   Installing the current project: fastapi_ecom (0.1.0)
7. Make changes to correctly configure the required variables for database and alembic initialization
   Command
   ```shell
   (venv) $ mv db_creds.py.example db_creds.py
   ```
   Change the variables as per your requirement
   ```
   name = <DATABASE-NAME>
   user = <DATABASE-USER>
   password = <DATABASE-PASSWORD>
   host = <HOST>
   port = <PORT>
   ```
   Command
   ```shell
   (venv) $ mv alembic.ini.example alembic.ini
   ```
   Change `sqlalchemy.url` with the above user variables
   ```
   sqlalchemy.url = postgresql+asyncpg://<DATABASE-USER>:<DATABASE-PASSWORD>@<HOST>:<PORT>/<DATABASE-NAME>
   ```
8. Create the required database structure using `alembic` migration.  
   Command
   ```shell
   (venv) $ alembic upgrade head
   ```
   Sample output
   ```shell
   INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
   INFO  [alembic.runtime.migration] Will assume transactional DDL.
   INFO  [alembic.runtime.migration] Running upgrade  -> 306d801996a6, initial model setup
   INFO  [alembic.runtime.migration] Running upgrade 306d801996a6 -> d6dd218459b7, change datatype of password column
   INFO  [alembic.runtime.migration] Running upgrade d6dd218459b7 -> 7d1eff027259, remove creation_date from base models and add using mixin
   INFO  [alembic.runtime.migration] Running upgrade 7d1eff027259 -> 97e78a849e66, add creation date mixin in orders
   INFO  [alembic.runtime.migration] Running upgrade 97e78a849e66 -> 29f5c5a0304d, modify date field mixin
   INFO  [alembic.runtime.migration] Running upgrade 29f5c5a0304d -> 60c8ccec25ac, create and update date with relation correction
   ```
9. Run the development server.  
   Command
   ```
   uvicorn main:app --reload
   ```
   Sample output
   ```shell
   INFO:     Will watch for changes in these directories: ['/home/sdglitched/FastAPI_eCom/fastapi_ecom']
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process [21520] using WatchFiles
   INFO:     Started server process [21522]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

## Usage
1. Default Route
   This is default FastAPI route which returns details related to this project.  
   ```
   {
      "title": "FastAPI ECOM",
      "description": "E-Commerce API for businesses and end users using FastAPI.",
      "version": "0.1.0"
   }
   ```
   ![](https://raw.githubusercontent.com/sdglitched/FastAPI-eCom/main/docs/imgs/default_enpt.png)
2. Business Route  
   This route contains endpoints for performing CRUD operations on business entity.  
   `create`: Endpoint to create a new business account. No authentication is needed for connecting to this endpoint.  
   `me`: It is a endpoint to fetch the email of the currently authenticated business.  
   `search`: Endpoint to fetch a paginated list of businesses from the database. No authentication is needed for connecting to this endpoint.  
   `delete`: Endpoint for an authenticated business to delete its own record.  
   _Note:_ This endpoint will be depricated in future update with the implementation of archiving.  
   `update`: Endpoint for an authenticated business to update its own record.  
   ![](https://raw.githubusercontent.com/sdglitched/FastAPI-eCom/main/docs/imgs/business_enpt.png)  
3. Product Route  
   This route contains endpoints for performing CRUD operations on product entity.  
   `create`: Endpoint to add a new product by currently authenticated business.  
   `search`: Endpoint fetches a paginated list of products from the database. No authentication is needed for connecting to this endpoint.  
   `search/name`: Endpoint fetches a paginated list of products by name or description. No authentication is needed for connecting to this endpoint.  
   `search/internal`: Endpoint fetches a paginated list of products associated with the authenticated business.  
   `search/uuid`: Endpoint fetches a specific product by its UUID (Product ID) associated with the authenticated business.  
   `delete/uuid`: Endpoint to delete a product by its UUID associated for an authenticated business.  
   _Note:_ This endpoint will be depricated in future update with the implementation of archiving.  
   `update/uuid`: Endpoint to update a product by its UUID associated for an authenticated business.  
   ![](https://raw.githubusercontent.com/sdglitched/FastAPI-eCom/main/docs/imgs/product_enpt.png)  
4. Customer Route  
   This route contains endpoints for performing CRUD operations on customer entity.  
   `create`: Endpoint to create a new customer account. No authentication is needed for connecting to this endpoint.  
   `me`: It is a endpoint to fetch the email of the currently authenticated customer.  
   `search`: Endpoint to fetch a paginated list of customers from the database. No authentication is needed for connecting to this endpoint.  
   `delete`: Endpoint for an authenticated customer to delete its own record.  
   `update`: Endpoint for an authenticated customer to update its own record.  
   ![](https://raw.githubusercontent.com/sdglitched/FastAPI-eCom/main/docs/imgs/customer_enpt.png)  
5. Order Route  
   This route contains endpoints for performing CRUD operations on order and order_details entities.  
   `create`: Endpoint to place an order by the authenticated customer.  
   `search`: Endpoint fetches a paginated list of orders and its details associated with the authenticated customer.  
   `search/internal`: Endpoint fetches a paginated list of orders and its details.  
   _Note:_ This endpoint is ment to be used by an admin account which will created in future update. Currently no authentication is needed for connecting to this endpoint.  
   `search/uuid`: Endpoint fetches a specific order and its details by its UUID associated with the authenticated customer.  
   `delete/uuid`: Endpoint to delete a order by its UUID associated for an authenticated customer.  
   _Note:_ This endpoint will be depricated in future update with the implementation of archiving.  
   ![](https://raw.githubusercontent.com/sdglitched/FastAPI-eCom/main/docs/imgs/order_enpt.png)  

## Future Roadmap
1. Implement _OIDC/OAuth2_ for authentication instead for HTTP Basic Auth.  
2. Implement _admin_ functionality across all the routes.  
3. Implement _archiving_ across all the routes instead of direct deletion from database.  
4. Implement _carting_ functionality while placing order.  
5. Implement some kind of verification for customers and businesses.  
