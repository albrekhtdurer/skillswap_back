# SkillSwap – Your Platform for Swapping Skills

Backend for SkillSwap, a social network that enables users to learn new skills and share their expertise with others. The frontend is available [here](LINK).

## Tech stack

- Python, FastAPI, SQLite, SQLAlchemy, Alembic

## Features

Supported features:

- Login and JWT access token generation.
- Register new users and update user data.
- Upload images (user avatars and skill images). Uploaded images are assigned new filenames, and a GET link is generated for each image.
- Retrieve skills, cities, and categories data.

## Dependencies

The application requires the following dependencies to launch:

- Python 3.12.3+
- Docker (optional if deploying via a Docker container)

## Local launch

1. Create and activate a virtual environment (recommended for correct dependency installation):

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run DB migrations:

```bash
alembic upgrade head
```

4. Run the server:

```bash
APP_SECRET=<secret> APP_HOST=127.0.0.1 APP_PORT=8000 uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The server will be available at `http://localhost:8000` or `http://127.0.0.1:8000`.

## Local launch via Docker

1. Run the container:

```bash
make up
```

The server will be available at `http://localhost:8000` or `http://0.0.0.0:8000`.

## Troubleshooting

If images don't upload correctly:

- Create the `/opt/uploaded_files` folder and grant the current user read/write access rights.
