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
* 🧇 Modular unit testing with [pytest](https://docs.pytest.org/)
* 🧹 Static analysis with [ruff](https://github.com/astral-sh/ruff) and [mypy](https://github.com/python/mypy)
* 🐳 Docker & Makefile for local development and production
* 🦷 Integrated [pre-commit](https://pre-commit.com/) hooks
* 🚀 CI/CD via GitHub Actions and DockerHub with auto-deploy on VPS using Watchtower

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

```bash
make develop
```

### 🐳 Run Dev Containers

```bash
make local
```

To stop:

```bash
make local_down
```

### 🏃 Start the Bot

```bash
make app
```

### 📊 Migrations

```bash
make local-apply-migrations     # Apply
make local-create-migrations    # Generate
make local-delete-migrations    # Delete all
```

---

## 📊 Code Quality

```bash
make lint    # run ruff with autofix
make mypy    # run static type checks
```

---

## 🥪 Testing

* `pytest`, `pytest-asyncio`, `pytest-cov`
* Test factories via `polyfactory`

---

## 🛠️ Environment Configuration

Example `.env.dev`:

```env
APP_DB_USER=mrfixit
APP_DB_PASSWORD=mrfixit
APP_DB_NAME=mrfixit
APP_DB_HOST=localhost
APP_DB_PORT=5432

APP_REDIS_HOST=localhost
APP_REDIS_PORT=6379
APP_REDIS_PASSWORD=mrfixit

APP_TG_BOT_TOKEN=...
APP_TG_ALLOWED_CHAT_ID=...
```

---

## 🚢 DockerHub, CI/CD & Autodeploy

### ⟳ GitHub Actions Workflow

CI/CD is handled via GitHub Actions:

* PR triggers `lint` and `test` jobs
* Merge to `main` triggers:

  * Docker image build and push to [DockerHub](https://hub.docker.com/repository/docker/ertiops/mrfixit)
  * Auto-deploy on VPS via [Watchtower](https://containrrr.dev/watchtower/)

### 🛆 DockerHub

Latest production image is available here:

```
docker pull ertiops/mrfixit:latest
```

### ⚙️ GitHub Secrets

The following secrets are used in CI:

* `DOCKERHUB_USERNAME`
* `DOCKERHUB_TOKEN`

They are used to authenticate and push images.

### 🛡️ Autodeploy with Watchtower

On the server, Watchtower is configured to track `ertiops/mrfixit:latest`.

Watchtower checks periodically and restarts the container when a new image is pushed:

```yaml
watchtower:
  image: containrrr/watchtower
  container_name: watchtower
  restart: unless-stopped
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
  command: --interval 60
```

The `mrfixit` container is defined like this:

```yaml
services:
  mrfixit:
    image: ertiops/mrfixit:latest
    container_name: mrfixit_app
    env_file:
      - .env
    ports:
      - "8001:8000"
    restart: unless-stopped
```

### 🧠 Apply Migrations Automatically

On container startup, the bot will apply DB migrations automatically using:

```bash
.venv/bin/python -m mrfixit.adapters.database upgrade head
```

No `entrypoint.sh` is needed — this logic is built into the image.

---

## 📂 Project Structure

```
mrfixit/
├─ adapters/       # DB, Redis, DI, storages, migrations
├─ application/    # Shared app config, exceptions
├─ domain/         # Entities, services, interfaces, utils
├─ presenters/     # Telegram bot: dialogs, handlers, messages
tests/             # Unit tests, test utils, factories
Makefile           # Development scripts
...
```

---

## 🧑‍💻 Author

Developed by Eljan T — [straxisrule@gmail.com](mailto:straxisrule@gmail.com)
