#!/usr/bin/env python3
from openai_decorator.openai_decorator import openaifunc, get_openai_funcs
from pydantic import BaseModel, Field

import openai
import os
import sys
import json

openai.api_key = os.getenv("OPENAI_API_KEY")


class LocationModel(BaseModel):
    location: str = Field(description="The name of the place in the real world")
    country: str = Field(description="The country in which to look for the place")


@openaifunc
def get_current_weather(location: LocationModel) -> str:
    """
    Gets the current weather information
    """
    location = LocationModel.parse_obj(location)
    if location is None:
        return "A location must be provided. Please ask the user which location they want the weather for"
    if location.country == "France":
        return "The weather is terrible, as always"
    else:
        return "The weather is nice and sunny"


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
