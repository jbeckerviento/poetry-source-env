# Changelog[^1]

All notable changes to poetry-source-env will be documented here. Breaking changes are marked with a 🚩.

poetry-source-env adheres to [semantic versioning](https://semver.org/spec/v2.0.0.html).

## <a name="2-1-0">[2.1.0] - 2026-03-01</a>

### Fixed

- Added support for Poetry 2.3.x by widening the Poetry dependency range.

## <a name="2-0-3">[2.0.3] - 2026-02-28</a>

### Fixed

- Restored `tool.poetry.source` environment-variable expansion on Poetry 2.2.x by patching Poetry's project loader
  before source validation runs.
- Added support for Poetry 2.2.x for environment-defined sources by widening the Poetry dependency range.
- Removed the stale `default` source priority mapping so environment-defined priorities stay compatible with Poetry
  2.2.

### Changed

- Migrated package metadata and plugin entry points from legacy `[tool.poetry]` tables to `[project]`.

## <a name="2-0-2">[2.0.2] - 2026-02-28</a>

### Fixed

- Added support for Poetry 2.2.x for environment-defined sources by widening the Poetry dependency range.
- Removed the stale `default` source priority mapping so environment-defined priorities stay compatible with Poetry
  2.2.

### Changed

- Documented that Poetry 2.2.x validates `tool.poetry.source` entries before plugins activate, which limits how much
  of the TOML expansion workflow remains usable there.

## <a name="2-0-1">[2.0.1] - 2023-06-15</a>

### Fixed

- Fixed a bug where poetry-source-env would not acknowledge sources defined in `pyproject.toml` with a priority of
  `explicit`. (celsiusnarhwal/poetry-source-env#2)

## <a name="2-0-0">[2.0.0] - 2023-05-23</a>

### Added

- Source priority can now be configured via environment variables. For example:

  ```bash
  export POETRY_REPOSITORIES_FOO_URL=https://foo.bar/simple
  export POETRY_REPOSITORIES_FOO_PRIORITY=primary
  ```

  poetry-source-env does not allow the `secondary` priority to be set via environment variables as Poetry has
  deprecated it.

  For more information, see [Poetry's documentation](https://python-poetry.org/docs/repositories/#package-sources).

### Changed

- 🚩 poetry-source-env now requires Poetry 1.5.0 or later. If you need support for Poetry 1.4 or earlier, use
  poetry-source-env 1.1.1.

### Removed

- 🚩 The `default` and `secondary` attributes of package sources are no longer configurable via environment variables
  following their deprecation in Poetry 1.5.0 (see celsiusnarhwal/poetry-source-env#1, python-poetry/poetry#7658).

## <a name="1-1-1">[1.1.1] - 2023-05-02</a>

### Fixed

- Fixed a bug where poetry-source-env would not respect the `prefix` setting for environment variables defining the
  priority of a source.

## <a name="1-1-0">[1.1.0] - 2023-05-01</a>

### Added

- poetry-source-env can now expand environment variables in the `tool.poetry.source` section of `pyproject.toml`.
  For example, this:

  ```bash
  export INDEX_URL="https://foo.bar/simple"
  ```

  ```toml
  [[tool.poetry.source]]
  name = "foo"
  url = "${INDEX_URL}"

  ```

  will now become:

  ```toml
  [[tool.poetry.source]]
  name = "foo"
  url = "https://foo.bar/simple"

  ```

- poetry-source-env's behavior can now be configured via the `tool.poetry-source-env` section of `pyproject.toml`.
  Available configuration options are documented in the [README](README.md#configuration).

## <a name="1-0-1">[1.0.1] - 2023-04-29</a>

No user-facing changes are introduced in this release.

## <a name="1-0-0">[1.0.0] - 2023-04-29</a>

This is the initial release of poetry-source-env.

[^1]: Based on [Keep a Changelog](https://keepachangelog.com).
