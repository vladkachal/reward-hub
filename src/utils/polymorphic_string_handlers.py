import json

from json import JSONDecodeError


class BoolOrDictHandlerError(Exception): ...


class BoolOrDictHandler:
    """
    Transforms polymorphic string, which may represent bool or dict types,
    to its actual type.

    Example:
        from decouple import config
        conf = config("DATABASE_POOL", cast=BoolOrDictHandler(), default=True)

        value = 'False'
        handler = BoolOrDictHandler()
        handler(value)
    """

    def __call__(self, value: str | bool | dict) -> bool | dict | None:
        """
        Transforms the given value into a Python object.

        Args:
            value (str | bool | dict): The input value.

        Returns:
            - `None` if the input is the empty string.
            - `False` if the input is the string 'False'.
            - `True` if the input is the string 'True'.
            - A dictionary if the input is a valid JSON-encoded dictionary.

        Raises:
            BoolOrDictHandlerError:
                If the input cannot be parsed as a boolean or JSON.
        """

        if isinstance(value, bool | dict):
            ret_value = value
        elif value == "":
            ret_value = None
        elif value == "False":
            ret_value = False
        elif value == "True":
            ret_value = True
        else:
            try:
                value = json.loads(value)
                ret_value = value
            except JSONDecodeError as exc:
                msg = f"Invalid input for BoolOrDictHandler: `{value}`"
                raise BoolOrDictHandlerError(msg) from exc
        return ret_value
