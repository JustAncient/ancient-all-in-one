# Ancient All-in-One

A modular desktop app for tracking daily, weekly, character, account,
and goal progression across games.

The first version focuses on a scalable foundation:

- Tkinter desktop shell with a Codex-like menu bar and left navigation.
- Persistent user data in `%LOCALAPPDATA%\Ancient All-in-One`.
- Timestamped backups for risky data operations.
- Goal submenus that can be created from the `+` button beside Goals.
- Separate services for storage, validation, settings, diagnostics, and updates.
- GitHub Releases update checker that preserves user data.

## Run

```powershell
& "C:\Users\Ancie\AppData\Local\Programs\Python\Python313\python.exe" -m ancient_all_in_one
```

## Check

```powershell
.\scripts\check.ps1
```

## Project Layout

```text
ancient_all_in_one/
  __main__.py
  app.py
  config.py
  models.py
  data/
    default_state.py
  migrations/
    __init__.py
  modules/
    registry.py
  services/
    backups.py
    diagnostics.py
    settings.py
    storage.py
    telemetry.py
    updates.py
    validation.py
  ui/
    main_window.py
    navigation.py
    pages.py
```

## Safety Docs

See [docs/development.md](docs/development.md) for testing, logging, and user
data safety notes.
See [docs/github_safety.md](docs/github_safety.md) for branch protection setup.
See [docs/update_flow.md](docs/update_flow.md) for the release checklist.
See [CHANGELOG.md](CHANGELOG.md) for version history.
