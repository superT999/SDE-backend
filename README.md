# Simple Database explorer - backend

## Features
- Fetching schemas
- Fetching tables from schema
- Fetching table content from table
- Implement backend pagination

## Tech Stacks
- Python & FastAPI
- Postgres & SQLAlchemy

## Dev environment setup

### Dependencies

- Python 3.11
- Postgres (credentials are stored inside `.env`)
- run command `pip install -r requirements.txt` inside venv

### Linting

run `black .` before commit

### How to run

- run command `uvicorn main:app` to run the server
- database/migration includes the migration scripts, should run it manually at this point