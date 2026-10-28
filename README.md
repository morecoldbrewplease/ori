# Ori

A student productivity web app built with Django.

## Apps

| App | Purpose |
| --- | --- |
| `accounts` | Custom user model and authentication |
| `dashboard` | Overview page |
| `calendar_app` | Calendar and events |
| `tasks` | To-do tasks |
| `pomodoro` | Pomodoro focus timer |
| `subjects` | School subjects |
| `stats` | Statistics |

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```sh
uv sync
cp .env.example .env   # then set DJANGO_SECRET_KEY (command is in the file)
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Open http://127.0.0.1:8000/admin/ to log in.

## Development

Install the git hooks once, so ruff lints and formats code on each commit:

```sh
uv run pre-commit install
```
