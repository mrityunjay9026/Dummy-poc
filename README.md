# API Collections Manager

A FastAPI application for managing Postman API collections with SQLite and SQLAlchemy.

## Features

- Store and retrieve Postman collections
- Search APIs by name
- RESTful endpoints
- Comprehensive testing with pytest
- Code quality gates with multiple linters
- CI/CD with GitHub Actions

## Requirements

- Python 3.11

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `uvicorn app.main:app --reload`

## API Endpoints

- `GET /v1/health` - Health check
- `GET /v1/apis` - List all APIs
- `GET /v1/apis/{id}` - Get API by ID
- `GET /v1/apis/name/{name}` - Get API by name
- `GET /v1/apis/{id}/collection` - Get Postman collection JSON
- `GET /v1/apis/search?query={query}` - Search APIs by name

## Development

Run tests: `pytest`

Format code: `black .`

Sort imports: `isort .`

Lint: `flake8`, `pylint`, `mypy`

Security: `bandit`, `pip-audit`

## CI/CD

GitHub Actions workflow includes:
- Code formatting (black, isort)
- Linting (flake8, pylint, mypy)
- Security checks (bandit, pip-audit)
- CodeQL analysis
- SonarCloud integration

## Security Practices

- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- Logging instead of prints
- Dependency pinning
- Automated security scans