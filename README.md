# GPT-4 Function Python Decorator

This Python package creates a function decorator `@openaifunc` which can be used to automatically generate the `functions` parameter for the ChatGPT API.

This code was generated [with GPT-4](https://chat.openai.com/share/d32b7a1c-1b5d-4d2f-895e-edc2e6576164). I'm new to Python and have never created a Python package.

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
