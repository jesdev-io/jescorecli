# Changelog

## 1.0.5 - 2026-07-29

### Added
- 🔌 Support for old TTL232R probes
- 🧰 `uv` development workflow
- 🧹 Ruff linting configuration and cleanup

### Fixed
- 🔄 CLI receive/listen handling for keep-open operation
- 🚦 Compatibility with updated jescore error output

## 1.0.4 - 2026-05-20

### Fixed
- 🪲 Core messages now always propagate through filter
- 🔄 Board reset on CLI connect (matching PIO terminal behavior)

## 1.0.3 - 2025-04-15

### Added
- 🛣️ UART stream separation (available on `jescore` 2.3.0 firmware)

## 1.0.2 - 2025-11-23

### Fixed
- 🪲 Private method bug hotfix

## 1.0.1 - 2025-11-23

### Added
- ➡️ This changelog
- 📜 Better looking README

### Changed
- 🔆 Migration from main `jescore` repo to here
- 🖨️ Print statements now only occur on verbose and CLI usage, not API usage

