# 🛠️ MrFixIt — Telegram Bot for Tech Requests

A Telegram bot for creating and managing tech repair requests in small businesses.
Designed for staff and technical personnel in environments like escape room projects.

---

## ✨ Features

* ✅ Clean architecture with separation of concerns
* 🧩 Dependency Injection using [Dishka](https://github.com/reagento/dishka)
* 💬 Powered by [aiogram-dialog](https://github.com/Tishka17/aiogram_dialog) for structured conversation flows
* 🔄 Redis as FSM storage for user state management
* 🛠️ PostgreSQL for storing tech requests
* 🧵 Transaction management via Unit of Work pattern
* ⏰ Scheduled cleanup of processed requests using [aiomisc](https://aiomisc.readthedocs.io/)
* 🥪 Modular unit testing with [pytest](https://docs.pytest.org/)
* 🧹 Static analysis with [ruff](https://github.com/astral-sh/ruff) and [mypy](https://github.com/python/mypy)
* 🐳 Docker & Makefile for local development and production
* 🥷 Integrated [pre-commit](https://pre-commit.com/) hooks

---

## 🚀 Functional Overview

**User roles**: Staff members and technical team.
**Core capabilities**:

* Submit new tech requests via Telegram
* View the list of requests
* Inspect detailed info on individual requests
* Periodic deletion of processed requests via cron jobs

---

## ⚙️ Development Setup

### 📅 Install Dependencies

Use `make develop` to create a virtual environment and install dependencies:

```bash
make develop
```

### 🐳 Run Dev Containers

To launch Redis and PostgreSQL containers for development:

```bash
make local
```

To stop and remove dev containers:

```bash
make local_down
```

### 🏃 Start the Bot

To run the bot locally (via aiomisc entrypoint):

```bash
make app
```

### 📊 Code Quality

```bash
make lint    # run ruff with autofix
make mypy    # run mypy static type checker
```

### 📈 Apply Database Migrations

Make sure your `.env` is configured and containers are running.

```bash
make local-apply-migrations
```

### 🏗️ Create New Migration

```bash
make local-create-migrations
```

To delete all generated versions:

```bash
make local-delete-migrations
```

---

## 🛠️ Environment Configuration

Example `.env.dev`:

---

## 🥪 Testing

* Unit tests with `pytest` and `pytest-asyncio`
* Test factories with `polyfactory`
* Coverage reporting via `pytest-cov` and `coverage`

---

## 📦 Tech Stack

* Python 3.12
* aiogram 3.x + aiogram-dialog
* PostgreSQL + asyncpg + SQLAlchemy 2
* Redis
* aiomisc (scheduling, cron jobs)
* Dishka (DI container)
* Poetry + Make
* Docker / Docker Compose

---

## 📂 Project Structure

```
mrfixit/
├─ adapters/       # DB, Redis, DI, storages, migrations
├─ application/    # Shared app config, exceptions
├─ domain/        # Entities, services, interfaces, utils
├─ presenters/     # Telegram bot: dialogs, handlers, messages
tests/          # Unit tests, test utils, factories
Makefile        # Development scripts
...
```
---

## 🧑‍💻 Author

Developed by Eljan T — [straxisrule@gmail.com](mailto:straxisrule@gmail.com)
