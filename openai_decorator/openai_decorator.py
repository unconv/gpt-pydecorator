import inspect
import functools
from pydantic import BaseModel

# Global variable to store all functions decorated with @openaifunc
openai_functions = []

# Map python types to JSON schema types
type_mapping = {
    int: "integer",
    float: "number",
    str: "string",
    bool: "boolean",
    list: "array",
    tuple: "array",
    dict: "object",
    None: "null",
}


def get_params_dict(params):
    params_dict = {}
    print(params)
    for k, v in params.items():
        if issubclass(v.annotation, BaseModel):
            print(list(v.annotation.schema()["properties"].items()))
            params_dict[k] = {
                "type": "object",
                "properties": {
                    field_name: {
                        "type": property.get("type", "unknown"),
                        "description": property.get("description", ""),
                    }
                    for field_name, property in v.annotation.schema()[
                        "properties"
                    ].items()
                },
            }
        else:
            params_dict[k] = {
                "type": type_mapping.get(v.annotation, "unknown"),
                "description": "",
            }
    return params_dict


def openaifunc(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Get information about function parameters
    params = inspect.signature(func).parameters

    param_dict = get_params_dict(params)

    openai_functions.append(
        {
            "name": func.__name__,
            "description": inspect.cleandoc(func.__doc__ or ""),
            "parameters": {
                "type": "object",
                "properties": param_dict,
                "required": list(param_dict.keys()),
            },
        }
    )

    return wrapper


def get_openai_funcs():
    return openai_functions
