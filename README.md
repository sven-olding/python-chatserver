# Chat Server Example using FastAPI

This project is managed using [uv](https://github.com/astral-sh/uv)

## Running the application

### Development mode

```shell
uv run fastapi dev
```

### Production mode

```shell
uv run fastapi run
```

## Build Docker image

```shell
docker build -t chatserver .
```

## Run in Docker

```shell
docker run -p 8000:80 chatserver
```