from poetry.console.application import Application
from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_source_env.config import expand_poetry_sources

_PATCHED = False


def patch_pyproject_loader() -> None:
    global _PATCHED

    if _PATCHED:
        return

    from poetry.core.pyproject.toml import PyProjectTOML

    original_getter = PyProjectTOML.data.fget
    assert original_getter is not None

    def data(self: PyProjectTOML):
        pyproject = original_getter(self)

        if getattr(self, "_poetry_source_env_sources_expanded", False):
            return pyproject

        expand_poetry_sources(pyproject)
        setattr(self, "_poetry_source_env_sources_expanded", True)

        return pyproject

    PyProjectTOML.data = property(data)
    _PATCHED = True


class PoetrySourceApplicationPlugin(ApplicationPlugin):
    def activate(self, application: Application) -> None:
        super().activate(application)
        patch_pyproject_loader()
