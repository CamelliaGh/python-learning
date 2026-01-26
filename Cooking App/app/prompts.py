import os
import re


def load_template(template_name):
    """
    Load a template file from the 'static/prompts' directory.
    Automatically appends '.txt' to the filename.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    prompts_dir = os.path.join(base_dir, 'static', 'prompts')
    file_path = os.path.join(prompts_dir, f"{template_name}.txt")

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def render_template(template_str, variables):
    """
    Replace placeholders in the form {{VAR}} with values from variables.
    If a variable is missing, leave the placeholder unchanged and log a warning.
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


def render_prompt_from_file(template_name, variables):
    """
    Load a template from file, perform variable substitution, and return the final string.
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
