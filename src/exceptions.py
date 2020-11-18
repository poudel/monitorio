class MonError(Exception):
    """
    The base exception.
    """

    def __init__(self, message="", config=None):
        self.message = f"{self.__class__.__name__}: {message}"


class ConfigError(MonError):
    pass
