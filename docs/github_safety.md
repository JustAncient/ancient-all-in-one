# GitHub Safety Setup

These repository settings should be enabled before the project grows much more.

## Branch Protection

In GitHub, open:

```text
Settings > Branches > Add branch protection rule
```

Use this pattern:

```text
main
```

Recommended options:

- Require a pull request before merging.
- Require status checks to pass before merging.
- Select the `Tests` workflow check.
- Require branches to be up to date before merging.
- Do not allow force pushes.
- Do not allow deletions.

For solo development, pull requests can still be lightweight. The goal is to
make sure `main` always passes tests, lint, and compile checks.

## Releases

Use GitHub Releases as the public update source. Each release tag should match
`ancient_all_in_one/__init__.py`, for example:

```text
v0.2.0
```

## Data Safety

Never commit user data from `%LOCALAPPDATA%` or project-local `user_data/`.
The app stores backups in `%LOCALAPPDATA%\Ancient All-in-One\backups`.
