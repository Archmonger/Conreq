from typing import Type

from conreq.utils.environment import get_env


class EnvFieldMixin:
    """Generic field to read/write dot env values within a HTML form."""

    # pylint: disable= too-few-public-methods

    env_type: Type = str

    def __init__(self, env_name, *, required=False, **kwargs) -> None:
        super().__init__(required=required, **kwargs)  # type: ignore
        self.env_name = env_name

    def prepare_value(self, _):
        return get_env(
            self.env_name, default_value=self.initial, return_type=self.env_type  # type: ignore
        )
