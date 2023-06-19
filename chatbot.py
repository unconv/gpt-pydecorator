#!/usr/bin/env python3
from openai_decorator.openai_decorator import openaifunc, get_openai_funcs

import openai
import os
import sys
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

@openaifunc
def get_current_weather(location: str, country: str) -> str:
    """
    Gets the current weather information
    @param location: The location for which to get the weather
    @param country: The ISO 3166-1 alpha-2 country code
    """

    if country == "FR":
        return "The weather is terrible, as always"
    elif location == "California":
        return "The weather is nice and sunny"
    else:
        return "It's rainy and windy"


@openaifunc
def recommend_youtube_channel() -> str:
    """
    Gets a really good recommendation for a YouTube channel to watch
    """
    return "Unconventional Coding"


@openaifunc
def calculate_str_length(string: str) -> str:
    """
    Calculates the length of a string
    """
    return str(len(string))


# ChatGPT API Function
def send_message(message, messages):
    # add user message to message list
    messages.append(message)

    try:
        # send prompt to chatgpt
        response = openai.ChatCompletion.create(
            # model="gpt-4-0613",
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=get_openai_funcs(),
            function_call="auto",
        )
    except openai.error.AuthenticationError:
        print("AuthenticationError: Check your API-key")
        sys.exit(1)

    # add response to message list
    messages.append(response["choices"][0]["message"])

    return messages


# MAIN FUNCTION
def run_conversation(prompt, messages=[]):
    # add user prompt to chatgpt messages
    messages = send_message({"role": "user", "content": prompt}, messages)

    # get chatgpt response
    message = messages[-1]

    # loop until project is finished
    while True:
        if message.get("function_call"):
            # get function name and arguments
            function_name = message["function_call"]["name"]
            arguments = json.loads(message["function_call"]["arguments"])

            # call function dangerously
            function_response = globals()[function_name](**arguments)

            # send function result to chatgpt
            messages = send_message(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
                messages,
            )
        else:
            # if chatgpt doesn't respond with a function call, ask user for input
            print("ChatGPT: " + message["content"])

            user_message = input("You: ")

            # send user message to chatgpt
            messages = send_message(
                {
                    "role": "user",
                    "content": user_message,
                },
                messages,
            )

        # save last response for the while loop
        message = messages[-1]


# ASK FOR PROMPT
print(
    "Go ahead, ask for the weather, a YouTube channel recommendation or to calculate the length of a string!"
)
prompt = input("You: ")

# RUN CONVERSATION
run_conversation(prompt)
