# Contributing to Windscribe IP Changer for Android

Thanks for helping improve Windscribe IP Changer for Android!

## Code of Conduct

Please read and follow our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Development Setup

```bash
# Clone
git clone https://github.com/VoxHash/windscribe-ip-changer-android.git
cd windscribe-ip-changer-android

# Verify Python 3.x is installed
python3 --version

# Verify ADB is installed
adb version

# Run tests
python3 test_connection.py
```

## Project Structure

- `windscribe_ip_changer.py` - Main script
- `test_connection.py` - Connection test utility
- `example_usage.py` - Usage examples
- `servers.json.example` - Server configuration template
- `docs/` - Documentation

## Branching & Commit Style

- Branches: `feature/...`, `fix/...`, `docs/...`, `chore/...`
- Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

Examples:
- `feat: add support for custom ADB paths`
- `fix: correct device ID extraction`
- `docs: update installation instructions`

## Pull Requests

- Link related issues
- Add tests if applicable
- Update documentation
- Follow the PR template
- Keep diffs focused and reviewable
- Ensure code follows Python PEP 8 style guidelines

## Testing

Before submitting a PR:

1. Run `python3 -m py_compile windscribe_ip_changer.py` to check syntax
2. Test with a connected Android device or emulator
3. Run `python3 test_connection.py` to verify setup

## Release Process

- Semantic Versioning (MAJOR.MINOR.PATCH)
- Update [CHANGELOG.md](CHANGELOG.md) with changes
- Tag releases with version numbers
