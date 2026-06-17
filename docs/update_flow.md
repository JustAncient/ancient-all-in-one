# Update Flow

This project uses GitHub Releases as the update source.

The app checks this URL on launch and from `Help > Check for Updates`:

```text
https://api.github.com/repos/JustAncient/ancient-all-in-one/releases/latest
```

User data is stored outside the application package:

```text
user_data/tracker_data.json
```

That folder is ignored by Git, so code updates should not overwrite a user's
goals, notes, or custom sidebar items.

## Normal Development Loop

1. Make code changes locally.
2. Run tests:

   ```powershell
   & "C:\Users\Ancie\AppData\Local\Programs\Python\Python313\python.exe" -m unittest discover -s tests
   ```

3. Bump the version in `ancient_all_in_one/__init__.py`.
4. Commit the changes.
5. Push to GitHub:

   ```powershell
   git push
   ```

6. Create a GitHub release with a matching tag, such as `v0.1.1`.

## Release Checklist

- `ancient_all_in_one/__init__.py` has the new version.
- Tests pass locally.
- GitHub Actions passes on `main`.
- Release tag starts with `v`, for example `v0.2.0`.
- Release notes describe what changed.
- No user-specific files from `user_data/` are committed.

## Version Rules

Use semantic versions:

- Patch release: `0.1.1` for small fixes.
- Minor release: `0.2.0` for new tracker features.
- Major release: `1.0.0` when the app reaches a stable public shape.

## Future Installer Option

For now, updates open the GitHub release page. Later, the release can include a
packaged `.exe` built with PyInstaller. The same update checker can point users
to that release asset while preserving `user_data/`.
