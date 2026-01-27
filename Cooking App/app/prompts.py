"""Template loading and rendering utilities for prompt files.

This module provides functionality to load template files from the static/prompts
directory and perform variable substitution using a simple {{VAR}} placeholder syntax.
It is used primarily for generating prompts for AI services like OpenAI.
"""

import os
import re


def load_template(template_name: str) -> str:
    """Load a template file from the 'static/prompts' directory.

    Reads a text file template from the static/prompts directory. The .txt
    extension is automatically appended to the template name.

    Args:
        template_name: The name of the template file (without .txt extension).

    Returns:
        The contents of the template file as a string.

    Raises:
        FileNotFoundError: If the template file does not exist.
        IOError: If there is an error reading the file.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    prompts_dir = os.path.join(base_dir, 'static', 'prompts')
    file_path = os.path.join(prompts_dir, f"{template_name}.txt")

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def render_template(template_str: str, variables: dict) -> str:
    """Replace placeholders in the template string with variable values.

    Performs variable substitution on a template string using {{VAR}} syntax.
    Placeholders are matched using the pattern {{variable_name}} and replaced
    with corresponding values from the variables dictionary. If a variable is
    missing from the dictionary, the placeholder is left unchanged and a warning
    is printed to stdout.

    Args:
        template_str: The template string containing {{VAR}} placeholders.
        variables: A dictionary mapping variable names to their values.
            Values will be converted to strings during substitution.

    Returns:
        The template string with all found variables substituted. Placeholders
        for missing variables remain unchanged.

    Example:
        >>> template = "Hello {{name}}, you have {{count}} messages."
        >>> vars = {"name": "Alice", "count": 5}
        >>> render_template(template, vars)
        'Hello Alice, you have 5 messages.'
    """

    def replacer(match):
        var_name = match.group(1)
        if var_name in variables:
            return str(variables[var_name])
        else:
            print(f"Warning: Missing variable '{var_name}'")
            return match.group(0)  # Leave placeholder unchanged

    pattern = re.compile(r"\{\{(\w+)\}\}")
    return pattern.sub(replacer, template_str)


def render_prompt_from_file(template_name: str, variables: dict) -> str:
    """Load a template from file and render it with variable substitution.

    Convenience function that combines template loading and rendering. Loads
    a template file from static/prompts, performs variable substitution, and
    returns the final rendered string.

    Args:
        template_name: The name of the template file (without .txt extension).
        variables: A dictionary mapping variable names to their values for
            substitution in the template.

    Returns:
        The fully rendered template string with all variables substituted.

    Raises:
        FileNotFoundError: If the template file does not exist.
        IOError: If there is an error reading the template file.

    Example:
        >>> vars = {"ingredients": "chicken, rice", "meal_type": "dinner"}
        >>> prompt = render_prompt_from_file("recipe_prompt", vars)
    """
    template = load_template(template_name)

    result = render_template(template, variables)
    return result


if __name__ == "__main__":
    ingredients = {
        "ingredients": "Chicken, onion, tomatoes, garlic cloves, greek yogurt, rice, bread",
        "meal_type": "dinner"
    }
    rendered_prompt = render_prompt_from_file("recipe_prompt", ingredients)
    print("Rendered prompt:")
    print(rendered_prompt)
