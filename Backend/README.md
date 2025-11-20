# FastAPI + PostgreSQL Docker Application

A dockerized FastAPI application with PostgreSQL database.

## Quick Start

1. Start the application:
```bash
docker compose up --build
```

2. Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

## Docker Commands

```bash
# Start services
docker compose up

# Start in detached mode
docker compose up -d

# Build and start
docker compose up --build

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# View logs
docker compose logs

# View logs for specific service
docker compose logs api
docker compose logs db

# Restart services
docker compose restart
```

## API Endpoints

- `GET /` - Welcome message
- `POST /items/` - Create an item
- `GET /items/` - List all items
- `GET /items/{item_id}` - Get a specific item

## Development

The application uses hot-reload, so changes to the code will automatically restart the server.
