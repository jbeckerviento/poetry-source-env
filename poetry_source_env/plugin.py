import os
import re

from cleo.io.io import IO
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry
from poetry.repositories.legacy_repository import LegacyRepository
from poetry.repositories.repository_pool import Priority
from poetry_source_env.config import PSPConfig, expand_poetry_sources


class PoetrySourcePlugin(Plugin):
    def activate(self, poetry: Poetry, io: IO) -> None:
        config: PSPConfig = PSPConfig.load(poetry.pyproject.file)

        if config.env:
            repositories = {}
            pattern = re.compile(rf"{config.prefix}(?P<name>[A-Z_]+)_URL")

            for env_key in os.environ.keys():
                match = pattern.match(env_key)
                if match:
                    repositories[match.group("name").lower().replace("_", "-")] = {
                        "env_name": match.group("name"),
                        "url": os.environ[env_key],
                    }

            for name, repository in repositories.items():
                repo = LegacyRepository(name, repository["url"])

                priority_name = os.getenv(
                    f"{config.prefix}{repository['env_name']}_PRIORITY", "primary"
                )

                priorities = {
                    "primary": Priority.PRIMARY,
                    "supplemental": Priority.SUPPLEMENTAL,
                    "explicit": Priority.EXPLICIT,
                }

                priority = priorities.get(priority_name.casefold(), Priority.PRIMARY)

                poetry.pool.add_repository(repo, priority=priority)

        if config.toml:
            expand_poetry_sources(poetry.pyproject.data)

            for repository in poetry.get_sources():
                poetry.pool.remove_repository(repository.name)
                repo = LegacyRepository(repository.name, repository.url)
                poetry.pool.add_repository(repo, priority=repository.priority)
