# Ancient All-in-One

A modular desktop app for tracking daily, weekly, character, account,
and goal progression across games.

The first version focuses on a scalable foundation:

- Tkinter desktop shell with a Codex-like menu bar and left navigation.
- Persistent user data in `user_data/tracker_data.json`.
- Goal submenus that can be created from the `+` button beside Goals.
- Separate services for storage, navigation, and update checks.
- GitHub Releases update checker that preserves user data.

## Run

```powershell
& "C:\Users\Ancie\AppData\Local\Programs\Python\Python313\python.exe" -m ancient_all_in_one
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
  services/
    storage.py
    updates.py
  ui/
    main_window.py
    navigation.py
    pages.py
```

## Update Strategy

Keep user data outside the application package in `user_data/`. Ship code
updates through GitHub releases or a packaged installer, then run lightweight
data migrations on launch if the saved schema version is older than the app's
current schema.

See [docs/update_flow.md](docs/update_flow.md) for the full release checklist.
See [docs/development.md](docs/development.md) for testing, logging, and user
data safety notes.
