import inspect
import functools

# Global variable to store all functions decorated with @openaifunc
openai_functions = []

# Map python types to JSON schema types
type_mapping = {
    int: "integer",
    float: "number",
    str: "string",
    bool: "boolean",
    list: "array",
    dict: "object",
    None: "null",
}

def openaifunc(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Get information about function parameters
    params = inspect.signature(func).parameters

    param_dict = dict()
    for k, v in params.items():
        # Map python types to JSON schema types
        param_type = type_mapping.get(v.annotation, "unknown")

        param_dict[k] = {
            "type": param_type,
            "description": "",  # This would need to be manually added or extracted from docstring
        }

    openai_functions.append({
        "name": func.__name__,
        "description": inspect.cleandoc(func.__doc__ or ""),
        "parameters": {
            "type": "object",
            "properties": param_dict,
            "required": list(param_dict.keys()),
        },
    })

    return wrapper

def get_openai_funcs():
    return openai_functions
