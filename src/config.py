import os
from dataclasses import dataclass, fields, MISSING
from src.exceptions import ConfigError


@dataclass
class Config:
    """
    Encapsulates config parameters and allows for a cleaner way to
    pass it around the code.

    Supports default values and loading of values using environtment
    variables.
    """

    ENV_VAR_PREFIX = "MON"

    SQLITE_DB_PATH: str
    FREQUENCY_SECONDS: int = 6
    SERVICE_URL: str = "http://localhost:12345"
    HEALTHY_STATUS: int = 200
    REQUEST_TIMEOUT_SECONDS: int = 3
    REPORT_WAY_BACK_MINUTES: int = 10

    @classmethod
    def from_environment(cls):
        values = {}
        missing = []

        for field in fields(cls):
            env_var_name = f"{cls.ENV_VAR_PREFIX}_{field.name}"

            if field.default != MISSING:
                value = field.default
            else:
                value = None

            value = os.environ.get(env_var_name, value)
            if value is None:
                missing.append(env_var_name)
                continue

            try:
                values[field.name] = field.type(value)
            except ValueError:
                raise ConfigError(f"Can't convert config value '{value}' to {field.type}")

        if missing:
            raise ConfigError(
                "Missing environment var values for: {}".format(", ".join(missing))
            )
        return cls(**values)
