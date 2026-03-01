from collections.abc import MutableMapping
from os.path import expandvars
from typing import Any

from dict_deep import deep_get
from poetry.toml.file import TOMLFile
from pydantic import BaseSettings, validate_arguments
from typing_extensions import Self


class PSPConfig(BaseSettings):
    prefix: str = "POETRY_REPOSITORIES_"
    env: bool = True
    toml: bool = True

    @classmethod
    def load_pyproject(cls, pyproject: MutableMapping[str, Any]) -> Self:
        return cls.parse_obj(deep_get(pyproject, "tool.poetry-source-env") or {})

    @classmethod
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def load(cls, file: TOMLFile) -> Self:
        return cls.load_pyproject(file.read())


def expand_poetry_sources(pyproject: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
    config = PSPConfig.load_pyproject(pyproject)

    if not config.toml:
        return pyproject

    tool = pyproject.get("tool")
    if not isinstance(tool, MutableMapping):
        return pyproject

    poetry = tool.get("poetry")
    if not isinstance(poetry, MutableMapping):
        return pyproject

    sources = poetry.get("source")
    if not isinstance(sources, list):
        return pyproject

    for source in sources:
        if not isinstance(source, MutableMapping):
            continue

        for key in ("name", "url"):
            value = source.get(key)
            if isinstance(value, str):
                source[key] = expandvars(value)

    return pyproject
