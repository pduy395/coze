# Coze Installation Guide

This repository contains the sources clone some function of website [coze](https://www.coze.com/home). Here is guide instruction document of backend and database.

* Backend use [FastAPI](https://fastapi.tiangolo.com/) - web framework for building APIs with Python based on standard Python type hints
* Database use [Supabase](https://supabase.com/) - Supabase is an open source Firebase alternative, Postgre database.

## Repository structure

```
|-- README.md
|-- requirements.txt ....................... 1.
|-- .gitignore ......................... 2.
`-- test ....................... 3.
    |-- .......................
`-- app ....................... 4.
    `-- database ......................... 5.
        |-- db_service
    `-- helper ......................... 6.     
    `-- migrations ......................... 7.
    `-- models ......................... 8.
    `-- repository ......................... 9.
    `-- router ......................... 10.
    `-- schemas ......................... 11.
    `-- service ......................... 12.
    `-- utils ......................... 13.
    |-- .env ......................... 14.
    |-- main.py ......................... 15.
```

1. requirement libraries.
2. .gitignore
3. A folder to test api and function.
4. Contain entire source code.
5. Folder defines db service and db conection dependency
6. **helper** definition large language models Apis calller
7. **migrations** contains muilti versions of db 
8. **models** contains classes represent relations in database
9. **repository** define ORM query interact to database.
10. **router** contains router define APis endpoint
11. **schemas**  contains Pydantic schema modules.
12. **service** Contains modules for interacting with external services.
13. **utils** Contains utility modules.
14. Set up your environment variables in the `.env` file. You need to provide some LLM keys and secret key from Supabase.  
```
GOOGLE_API_KEY=
OPENAI_API_KEY=
COHERE_API_KEY=

SUPABASE_URL=
SUPABASE_SECRET_KEY=e
SQLALCHEMY_DATABASE_URL=

LLM_STUDIO_URL=
LLM_STUDIO_KEY=
```

## How to install

**Place the cursor in the directory /backend/app/**
```
$ cd backend/app
```
 
* To install python packages and libraries, run:

```
$ pip install -r requirement.txt
```
* To create a new alembic migartion database, run:
```
$ alembic revision --autogenerate
```

* To migrate database to cloud supabase, run:
```
$ alembic upgrade head
```

* To run FastAPI application with optional port and host, run:
```
$ uvicorn main:app --host 127.0.0.1 --port 8000 
```
### Run a LLM locally 
* If you run a LLM locally, download [LLM Studio](https://lmstudio.ai/) and set up key on your LLM Studio server.

* Then, download LLM model and add it to list models in ./router/chatbot


## Documentation
FastAPI provides automatic interactive API documentation using [Swagger](https://swagger.io/). Once the application is running, you can view the documentation at http://127.0.0.1:8000/docs.
