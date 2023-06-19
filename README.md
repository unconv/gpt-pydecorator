# GPT-4 Function Python Decorator

This Python package creates a function decorator `@openaifunc` which can be used to automatically generate the `functions` parameter for the ChatGPT API.

The original code was generated [with GPT-4](https://chat.openai.com/share/d32b7a1c-1b5d-4d2f-895e-edc2e6576164). I'm new to Python and have never created a Python package.

Inspired by @memespdf on @sentdex [YouTube-video](https://www.youtube.com/watch?v=0lOSvOoF2to) comments

## How to use

First, import the package at the top of your Python code:
```python
from openai_decorator.openai_decorator import openaifunc, get_openai_funcs
```

Then, add a `@openaifunc` decorator to the functions you want to use with ChatGPT:
```python
@openaifunc
def add_numbers(a: int, b: int):
    """
    This function adds two numbers.
    """
    return a + b
```

Then, you can get a list of all the functions and their definitions for ChatGPT with `get_openai_funcs()` like so:

```python
response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=messages,
    functions=get_openai_funcs(),
    function_call="auto",
)
```

## Parameter descriptions

As far as I know, there is no "official" way to add docstrings for parameters in Python, but you can add the parameter definitions to the docstring in PHP DocBlock style, and GPT-4 seems to obey them.

```python
@openaifunc
def get_current_weather(location: str, country: str) -> str:
    """
    Gets the current weather information
    @param location: The location for which to get the weather
    @param country: The country in which to look for the location
    """

    if location is None:
        return "A location must be provided. Please ask the user which location they want the weather for"
    else:
        return "The weather is nice and sunny"
```

Currently, this will not populate the `description` of the parameters in the API request, but GPT-4 still adheres to the rules.

## Pydantic Models

You can also set descriptions for the function parameters with Pydantic models. This will actually populate the `description` of the parameters in the API request.

```python
from pydantic import BaseModel, Field

class LocationModel(BaseModel):
    location: str = Field(
        description="The location for which to get the weather"
    )
    country: str = Field(
        description="The country in which to look for the location"
    )

@openaifunc
def get_current_weather(location: LocationModel) -> str:
    """
    Gets the current weather information
    """
    location = LocationModel.parse_obj(location)

    if location is None:
        return "A location must be provided. Please ask the user which location they want the weather for"
    else:
        return "The weather is nice and sunny"
```

## Chatbot

There's a demo chatbot that uses the GPT-4 API with function calling. You can run it by exporting your OpenAI API key first:

```console
$ export OPENAI_API_KEY=YOUR_API_KEY
```

And then running the script:
```console
$ ./chatbot.py
```

You can test it by asking it about the weather, some YouTube channel recommendations or to calculate the length of a string.

You can also modify the functions in the chatbot code, to test your own functions.
