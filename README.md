## What kind of project is this?
This is an API with 5 endpoints. Realistic AAA (Authentication Authorization and Accounting) server and implemented JWT.

## What technologies have I used?
- Python
  - FastAPI
  - SQLAlchemy
  - Pydantic
- JWT
- PostgreSQL
- Redis
- Docker

## Why did I even start creating this project?
This is a project created to study FastAPI. Also, with the help of this project, I studied (and am still studying): Docker, JWT token, AAA server.

## How usage?
For start project `uvicorn app.main:app --reload`

You can send requests for book:
- **GET** `/books/` - all info;
- **POST** `/books/` - add new book;
- **GET** `/books/id_book` - info about a specific book;
- **PUT** `/books/id_book` - update info about a specific book;
- **DELETE** `/books/id_book` - delete info about a specific book.

Requests for auth:
- **POST** `/auth/register` - user registrator;
- **POST** `/auth/login` - login for user;
- **POST** `/auth/refresh` - refresh access token;
- **POST** `/auth/logout` - logout account;
- **GET** `/auth/me` - information about you.

Requests for admin:
- **GET** `/admin/all_users` - information about all users;
- **PUT** `/admin/update_user_role` - update role for user;
- **DELETE** `/admin/delete_user` - delete user.

You can also use `/docs` to check the sending of requests, where all the endpoints will be

## How usage Docker?
1. Download git and docker to your server
2. Clone the entire project from the github - `git clone <link>`
3. Then use docker-compose to run the project - `docker-compose up`
