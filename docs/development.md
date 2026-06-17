# Development Safety

This project should stay easy to grow without risking user data.

## Local Commands

Run these before committing:

```powershell
& "C:\Users\Ancie\AppData\Local\Programs\Python\Python313\python.exe" -m unittest discover -s tests
& "C:\Users\Ancie\AppData\Local\Programs\Python\Python313\python.exe" -m compileall ancient_all_in_one tests
```

GitHub Actions also installs Ruff and runs:

```powershell
python -m ruff check ancient_all_in_one tests
```

## User Data

Normal user data lives in:

```text
%LOCALAPPDATA%\Ancient All-in-One\tracker_data.json
```

The app can adopt the old project-local file from:

```text
user_data\tracker_data.json
```

Saved data is written through a temporary file and then atomically replaced.
If JSON loading fails, the broken file is moved aside with a `.corrupt-*`
suffix and a fresh default state is created.

## Logging

Logs live in:

```text
%LOCALAPPDATA%\Ancient All-in-One\logs\app.log
```

Logs rotate automatically after roughly 1 MB, keeping three backups.

## Release Discipline

- Keep `main` green.
- Keep user data out of Git.
- Bump `ancient_all_in_one/__init__.py` before each release.
- Create a matching GitHub release tag, such as `v0.2.0`.
- Use storage migrations instead of replacing saved data.
