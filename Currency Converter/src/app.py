import streamlit as sl
from constants import CURRENCIES
from curreny_convertor import CurrencyConvertor

# Streamlit UI setup
sl.title(':dollar: Currency Converter')

sl.markdown("""
This tool allows you to instantly convert amounts between different currencies 🌍.

Enter the amount and choose the currencies to see the result.
""")

# User input fields
base_currency = sl.selectbox('From currency (Base):', CURRENCIES, index=0)
target_currency = sl.selectbox('To currency (Target):', CURRENCIES)
amount = sl.number_input("Please enter the amount", min_value=0.0, value=1.0)

# Initialize converter and perform conversion
curreny_convertor = CurrencyConvertor()

if amount > 0 and base_currency and target_currency:
    converted_amount = curreny_convertor.convert(
    amount, base_currency, target_currency)
    # Display results in three columns
    col1, col2, col3 = sl.columns(3)
    col1.metric(label="Base Currency", value=f"{amount:.2f} {base_currency}")
    col2.markdown("<h1 style='text-align: center; margin: 0; color: green;'>&#8594;</h1>", unsafe_allow_html=True)
    col3.metric(label="Target Currency", value=f"{converted_amount:.2f} {target_currency}")
