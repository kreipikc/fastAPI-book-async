## What kind of project is this?
This is an API with 5 endpoints.

## What technologies have I used?
- Python
  - FastAPI
  - SQLAlchemy
  - Pydantic
- PostgreSQL
- Docker

## Why did I even start creating this project?
This is a project created to study FastAPI.

## How usage?
For start project `uvicorn app.main:app --reload`

You can send requests:
- **GET** `/book/` - all info;
- **POST** `/book/` - add new book;
- **GET** `/book/id_book` - info about a specific book;
- **PUT** `/book/id_book` - update info about a specific book;
- **DELETE** `/book/id_book` - delete info about a specific book.

You can also use `/docs` to check the sending of requests, where all the endpoints will be

## How usage Docker?
1. Download git and docker to your server
2. Clone the entire project from the github - `git clone <link>`
3. Then use docker-compose to run the project - `docker-compose up`
