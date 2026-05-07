# ISUKU

ISUKU is a Django-based web application with modules for accounts, analytics, locations, notifications, reports, routing, and schedules.

## Features

- User authentication (register/login)
- Role-based dashboard redirects
- Contractor/admin/citizen analytics views
- Reports creation and management
- Routing and schedule pages
- Notifications and location overviews

## Project Structure

- `config/` - Django project settings and root URL configuration
- `accounts/` - authentication models, forms, and views
- `analytics/` - dashboard and role-based analytics views
- `locations/` - location models and overview pages
- `notifications/` - notification models and user pages
- `reports/` - reporting models, forms, and report workflows
- `routing/` - route details and contractor routing dashboard
- `schedules/` - schedule-related models and pages
- `templates/` - HTML templates
- `static/` - CSS and JavaScript assets

## Requirements

- Python 3.12+
- pip
- virtual environment support (`venv`)

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install django
python manage.py migrate
python manage.py runserver
```

Open the app at `http://127.0.0.1:8000/`.

## Development Notes

- Local database (`db.sqlite3`) is ignored in git.
- Virtual environment (`.venv/`) is ignored in git.
- Environment files (`.env*`) are ignored except `.env.example`.

## License

No license file is currently defined for this repository.
