# Chat Server Example using FastAPI

This project is managed using [uv](https://github.com/astral-sh/uv)

## Running the application

```shell
uv run fastapi dev
```

## Build Docker image

```shell
docker build -t chatserver .
```

## Run in Docker

```shell
docker run -p 8000:80 chatserver
```