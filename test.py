#!/usr/bin/env python3

# TEST FOR GPT-PYDECORATOR USAGE:
#
# Test format of get_openai_funcs():
# ./test.py
#
# Test response from ChatGPT:
# ./test.py api

from openai_decorator.openai_decorator import openaifunc, get_openai_funcs

import json
import sys

@openaifunc
def add_numbers(a: int, b: int):
    """
    This function adds two numbers.
    """
    return a + b

@openaifunc
def say_hello(name: str):
    """
    This function greets the user.
    """
    return f"Hello, {name}!"

@openaifunc
def save_numbers(count: int, numbers: tuple[int]):
    """
    Save some numbers to the database. Set count to the number of numbers the user asked for and numbers to the list of actual numbers
    @param count: Number of numbers to save
    @param numbers: The numbers
    """
    return (count, numbers)

@openaifunc
def list_synonyms(synonyms: list[str]):
    """
    Show a list of synonyms to the user
    """
    return synonyms

# OpenAI API doesn't seem to support this yet
# @openaifunc
# def triplet_test(triplet: tuple[int, str, float]):
#     """
#     Test a multi-type tuple
#     """
#     return triplet

# OpenAI API doesn't seem to support this yet
# @openaifunc
# def triple_list_test(triple_list: list[int, str, float]):
#     """
#     Test a multi-type list
#     """
#     return triple_list

funcs = get_openai_funcs()
print(json.dumps(funcs, indent=4))

expected = [
    {
        "name": "add_numbers",
        "description": "This function adds two numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "integer",
                    "description": ""
                },
                "b": {
                    "type": "integer",
                    "description": ""
                }
            },
            "required": [
                "a",
                "b"
            ]
        }
    },
    {
        "name": "say_hello",
        "description": "This function greets the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": ""
                }
            },
            "required": [
                "name"
            ]
        }
    },
    {
        "name": "save_numbers",
        "description": "Save some numbers to the database. Set count to the number of numbers the user asked for and numbers to the list of actual numbers\n@param count: Number of numbers to save\n@param numbers: The numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "description": ""
                },
                "numbers": {
                    "type": "array",
                    "description": "",
                    "items": {
                        "type": "integer"
                    }
                }
            },
            "required": [
                "count",
                "numbers"
            ]
        }
    },
    {
        "name": "list_synonyms",
        "description": "Show a list of synonyms to the user",
        "parameters": {
            "type": "object",
            "properties": {
                "synonyms": {
                    "type": "array",
                    "description": "",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": [
                "synonyms"
            ]
        }
    }
]

if expected != funcs:
    print("Test failed!")
    sys.exit(1)

if len(sys.argv) > 1:
    if sys.argv[1] != "api":
        print(f"ERROR: Invalid argument '{sys.argv[1]}'")
        sys.exit(1)

    import openai
    import os
    import re

    openai.api_key = os.getenv("OPENAI_API_KEY")

    test_messages = [
        {
            "function": "list_synonyms",
            "regex": r'\{\s*"synonyms"\s*:\s*\[\s*"(.*?)",\s*"(.*?)",\s*"(.*?)",\s*"(.*?)",\s*"(.*?)"\s*\]\s*\}',
            "message": {
                "role": "user",
                "content": "Give me 5 synonyms for 'amazing'"
            }
        },
        {
            "function": "save_numbers",
            "regex": r'\{\s*"count":\s*4,\s*"numbers":\s*\[0,\s*1,\s*1,\s*2\]\n\}',
            "message": {
                "role": "user",
                "content": "Save 4 fibonacci numbers to the database"
            }
        },
        {
            "function": "add_numbers",
            "regex": r'\{\s*"a":\s*42069420,\s*"b":\s*6969420\s*\}',
            "message": {
                "role": "user",
                "content": "What is 42069420 + 6969420?"
            }
        },
    ]

    for test in test_messages:
        response = openai.ChatCompletion.create(
            # model="gpt-4-0613",
            model="gpt-3.5-turbo-0613",
            messages=[test["message"]],
            functions=get_openai_funcs(),
            function_call="auto",
        )

        print(response)

        if not re.search(test["regex"], response["choices"][0]["message"]["function_call"]["arguments"]):
            print("Test failed!")
            sys.exit(1)

print("Test passed!")
sys.exit(0)
