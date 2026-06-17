# Development Safety

This project should stay easy to grow without risking user data.

## Local Commands

Run all local checks before committing:

```powershell
.\scripts\check.ps1
```

The script runs:

```powershell
python -m unittest discover -s tests
python -m compileall ancient_all_in_one tests
python -m ruff check ancient_all_in_one tests
```

## User Data

Normal user data lives in:

```text
%LOCALAPPDATA%\Ancient All-in-One\tracker_data.json
```

Settings live separately:

```text
%LOCALAPPDATA%\Ancient All-in-One\settings.json
```

The app can adopt the old project-local file from:

```text
user_data\tracker_data.json
```

Saved data is written through a temporary file and then atomically replaced.
If JSON loading fails, the broken file is moved aside with a `.corrupt-*`
suffix and a fresh default state is created.

## Backups

Backups live in:

```text
%LOCALAPPDATA%\Ancient All-in-One\backups
```

Backups are created before import operations and before future schema
migrations. Backup filenames include a timestamp and reason, such as
`tracker_data-20260617-120000-000000-pre-import.json`.

## Import / Export

Use `File > Export Data...` to copy tracker data to a user-selected JSON file.
Use `File > Import Data...` to validate and replace tracker data after creating
a backup of the existing file.

## Logging

Logs live in:

```text
%LOCALAPPDATA%\Ancient All-in-One\logs\app.log
```

Logs rotate automatically after roughly 1 MB, keeping three backups. Unhandled
Tkinter callback errors are logged and shown with a friendly error dialog.

## Migrations

Schema migrations belong in `ancient_all_in_one/migrations`. If
`SCHEMA_VERSION` increases, add a migration and tests before releasing. Missing
migrations intentionally fail rather than guessing.

## Release Discipline

- Keep `main` green.
- Keep user data out of Git.
- Run `scripts/check.ps1` before committing.
- Bump `ancient_all_in_one/__init__.py` before each release.
- Create a matching GitHub release tag, such as `v0.2.0`.
- Use storage migrations instead of replacing saved data.
