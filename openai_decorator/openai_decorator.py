import inspect
import functools
import importlib.util

# Global variable to store all functions decorated with @openaifunc
openai_functions = []

# Map python types to JSON schema types
type_mapping = {
    "int": "integer",
    "float": "number",
    "str": "string",
    "bool": "boolean",
    "list": "array",
    "tuple": "array",
    "dict": "object",
    "None": "null",
}

def get_type_mapping(param_type):
    param_type = param_type.replace("<class '", '')
    param_type = param_type.replace("'>", '')
    return type_mapping.get(param_type, "string")

def get_params_dict(params):
    params_dict = {}
    # Add optional pydantic support
    pydantic_found = importlib.util.find_spec("pydantic")
    if pydantic_found:
        from pydantic import BaseModel
    for k, v in params.items():
        if pydantic_found:
            if issubclass(v.annotation, BaseModel):
                # Consider BaseModel fields as dictionaries
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
            continue
        else:
            annotation = str(v.annotation).split("[")

            try:
                param_type = annotation[0]
            except IndexError:
                param_type = "string"

            try:
                array_type = annotation[1].strip("]")
            except IndexError:
                array_type = "string"

            param_type = get_type_mapping(param_type)
            params_dict[k] = {
                "type": param_type,
                "description": "",
            }

            if param_type == "array":
                if "," in array_type:
                    array_types = array_type.split(", ")
                    params_dict[k]["prefixItems"] = []
                    for i, array_type in enumerate(array_types):
                        array_type = get_type_mapping(array_type)
                        params_dict[k]["prefixItems"].append({
                            "type": array_type,
                        })
                else:
                    array_type = get_type_mapping(array_type)
                    params_dict[k]["items"] = {
                        "type": array_type,
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
