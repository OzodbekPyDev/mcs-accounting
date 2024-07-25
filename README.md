# MCS Accounting

## Overview
MCS Accounting is a robust accounting system built using modern Python web development frameworks and design principles. The project leverages **FastAPI** for the web framework, **SQLAlchemy** for database interaction, **Alembic** for migrations, and follows **Domain-Driven Design (DDD)** and **Clean Architecture (CA)** principles for a well-organized codebase.

## Features
- **FastAPI:** High-performance web framework for building APIs.
- **SQLAlchemy:** SQL toolkit and ORM for database interactions.
- **Alembic:** Database migrations for schema management.
- **DDD and CA:** Organized code with a clear separation of concerns.

## Getting Started

### Prerequisites
- Docker
- Docker Compose
- Python 3.x

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/OzodbekPyDev/mcs-accounting.git
   cd mcs-accounting
   ```

2. **Set up the environment:**
   - Create a `.env` file for environment variables based on `.env-test`.

3. **Build and run the Docker container:**
   ```bash
   docker-compose up --build
   ```

### Docs of API routers
Access the application via `http://localhost:8000/docs`.

## Contributing
Contributions are welcome! Please open issues or submit pull requests.

## License
This project is licensed under the MIT License.
```
