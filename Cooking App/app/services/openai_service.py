"""OpenAI API service for interacting with language models.

This module provides functionality to communicate with OpenAI-compatible APIs,
including prompt rendering, API calls, and error handling. It handles loading
environment variables, initializing the OpenAI client, and making chat completion
requests with customizable prompts and parameters.
"""

import logging
import os

from openai import APIError, OpenAI

from app.prompts import render_prompt_from_file
from app.config import OPENAI_DEFAULT_MODEL, OPENAI_DEFAULT_TEMPERATURE

# Load OpenAI credentials from environment (loaded by config.py)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def call_api(
    system_prompt_name,
    user_prompt_name,
    variables,
    model=OPENAI_DEFAULT_MODEL,
    temperature=OPENAI_DEFAULT_TEMPERATURE,
):
    """
    Renders prompts, sends them to the language model, and returns the response.

    Loads and renders system and user prompt templates from files, sends them
    to the OpenAI API, and returns the generated response. Handles various
    error conditions gracefully by logging errors and returning None.

    Args:
        system_prompt_name (str): Name of the system prompt template file
            (without .txt extension) located in static/prompts/.
        user_prompt_name (str): Name of the user prompt template file
            (without .txt extension) located in static/prompts/.
        variables (dict): Variables to fill into the prompt templates using
            {{variable_name}} placeholder syntax.
        model (str, optional): The language model to use. Defaults to "gpt-4o".
        temperature (float, optional): Sampling temperature for response creativity
            (0.0 to 2.0). Higher values make output more random. Defaults to 0.7.

    Returns:
        str or None: The language model's response content as a string (stripped
            of leading/trailing whitespace), or None if an error occurred.

    Raises:
        APIError: If the OpenAI API returns an error (caught and logged internally).
        FileNotFoundError: If a prompt template file cannot be found
            (caught and logged internally).
        OSError: If there is an error reading a prompt template file
            (caught and logged internally).
        IndexError: If the API response structure is unexpected
            (caught and logged internally).
        AttributeError: If the API response is missing expected attributes
            (caught and logged internally).

    Example:
        >>> variables = {"ingredients": "chicken, rice", "meal_type": "dinner"}
        >>> response = call_api("system_recipe_prompt", "user_recipe_prompt", variables)
        >>> if response:
        ...     print(response)
    """
    try:
        system_prompt = render_prompt_from_file(system_prompt_name, variables)
        user_prompt = render_prompt_from_file(user_prompt_name, variables)

        # Send prompts to the language model
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        return completion.choices[0].message.content.strip()

    except APIError as e:
        logging.error("LLM API Error: %s", e)
        return None
    except (FileNotFoundError, OSError) as e:
        logging.error("Error loading prompt template: %s", e)
        return None
    except (IndexError, AttributeError) as e:
        logging.error("Error parsing API response: %s", e)
        return None


if __name__ == "__main__":
    openai_model = os.environ.get("OPENAI_MODEL") or OPENAI_DEFAULT_MODEL
    call_api(
        "system_recipe_prompt",
        "user_recipe_prompt",
        {"onion"},
        openai_model,
        OPENAI_DEFAULT_TEMPERATURE,
    )
