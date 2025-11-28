import streamlit as st
from password_generator import RandomPasswordGenerator, PinGenerator, MemorablePassword


st.image("../images/password.png", width=100)
st.title(":zap: Password Generator")


option = st.radio("Select a passwprd generator",
                  ("Pin", "Memorable", "Random"))

if option == 'Pin':
    length = st.slider("Select the length of password", 4, 20, 6, 1)
    generator = PinGenerator(length)
elif option == 'Random':
    length = st.slider("Select the length of password", 4, 20, 6, 1)
    include_numbers = st.toggle("Include Numbers")
    include_punctuation = st.toggle("Include Punctuations")
    generator = RandomPasswordGenerator(
        length, include_numbers, include_punctuation)
else:
    num_of_words = st.slider("Select number of words", 4, 20, 6, 1)
    separator = st.text_input("Enter your favorite separator", "-")
    generator = MemorablePassword(num_of_words, separator=separator)

password = generator.generate()
st.write(f"Your password is ```{password}```")
