"""Streamlit app for generating passwords using Pin, Random, and Memorable strategies."""
import streamlit as st
from password_generator import PasswordGenerator, RandomPasswordGenerator, PinGenerator, MemorablePassword


def create_generator(option: str) -> PasswordGenerator:
    """Create and configure a password generator based on the selected option.

    Args:
        option: One of "Pin", "Memorable", or "Random".

    Returns:
        A `PasswordGenerator` configured from Streamlit UI inputs.
    """
    if option == 'Pin':
        length = st.slider("Select the length of password", 4, 20, 6, 1)
        return PinGenerator(length)
    elif option == 'Random':
        length = st.slider("Select the length of password", 4, 20, 6, 1)
        include_numbers = st.toggle("Include Numbers")
        include_punctuation = st.toggle("Include Punctuations")
        return RandomPasswordGenerator(length, include_numbers, include_punctuation)
    else:
        num_of_words = st.slider("Select number of words", 4, 20, 6, 1)
        separator = st.text_input("Enter your favorite separator", "-")
        return MemorablePassword(num_of_words, separator=separator)


def main() -> None:
    """Render the Streamlit UI and display the generated password."""
    st.image("../images/password.png", width=100)
    st.title(":zap: Password Generator")
    option = st.radio("Select a password generator", ("Pin", "Memorable", "Random"))
    generator = create_generator(option)
    password = generator.generate()
    st.write(f"Your password is ```{password}```")


if __name__ == "__main__":
    main()
